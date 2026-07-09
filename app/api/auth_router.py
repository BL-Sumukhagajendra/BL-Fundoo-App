from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth_schema import (
    RegistrationRequest,
    LoginRequest,
    LoginResponse,
    EmailVerificationRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.core.dependency import get_db

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register")
async def register(request: RegistrationRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    repository = UserRepository(db)
    service = AuthService(repository) 
    user, verification_token = await service.register_user(request)
    return {
        "message": "User registered successfully. Please verify your email.",
        "user_id": user.id,
        "verification_token_demo": verification_token
    }

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    repository = UserRepository(db)
    service = AuthService(repository)
    return await service.login(request.email, request.password)

@router.post("/verify-email")
async def verify_email(request: EmailVerificationRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    repository = UserRepository(db)
    service = AuthService(repository)
    message = await service.verify_email(request.token)
    return {"message": message}

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    repository = UserRepository(db)
    service = AuthService(repository)
    reset_token = await service.forgot_password(request.email)
    return {
        "message": "If the email exists, a password reset token has been generated.",
        "reset_token_demo": reset_token
    }

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Annotated[AsyncSession, Depends(get_db)]):
    repository = UserRepository(db)
    service = AuthService(repository)
    message = await service.reset_password(request.token, request.new_password)
    return {"message": message}
