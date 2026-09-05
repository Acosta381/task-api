from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str = Field(...,min_length=12)

class UserResponse(UserBase):
    id : int
    created_at : datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str

class RefreshTokenRequest(BaseModel):
    refresh_token : str