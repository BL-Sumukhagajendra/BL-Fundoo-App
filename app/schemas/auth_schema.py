from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class RegistrationRequest(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=100)]
    last_name: Annotated[str, Field(min_length=2, max_length=100)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

class EmailVerificationRequest(BaseModel):
    token: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: Annotated[str, Field(min_length=8)]
