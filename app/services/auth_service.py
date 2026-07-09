from fastapi import HTTPException
from starlette import status

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_temp_token,
    decode_temp_token
)
from app.schemas.auth_schema import RegistrationRequest
from app.repositories.user_repository import UserRepository

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, request: RegistrationRequest):
        existing_user = await self.user_repository.get_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        
        user = User(
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            password=hash_password(request.password)
        )
        created_user = await self.user_repository.create(user)
        
        # Generate verification token
        verification_token = create_temp_token(
            {"sub": user.email, "purpose": "email_verification"},
            expires_in_minutes=60
        )
        return created_user, verification_token
    
    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        
        if not verify_password(password, user.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")

        token = create_access_token(
            {"sub": str(user.id)}
        )
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    async def verify_email(self, token: str) -> str:
        email = decode_temp_token(token, required_purpose="email_verification")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if user.is_verified:
            return "Email is already verified"
            
        user.is_verified = True
        await self.user_repository.save(user)
        return "Email verified successfully"

    async def forgot_password(self, email: str) -> str:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist"
            )
        
        # Generate reset token valid for 15 minutes
        reset_token = create_temp_token(
            {"sub": email, "purpose": "password_reset"},
            expires_in_minutes=15
        )
        return reset_token

    async def reset_password(self, token: str, new_password: str) -> str:
        email = decode_temp_token(token, required_purpose="password_reset")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
            
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.password = hash_password(new_password)
        await self.user_repository.save(user)
        return "Password reset successfully"
