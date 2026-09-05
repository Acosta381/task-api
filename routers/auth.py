from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from core.limiter import limiter
from core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    verify_password,
)
from crud.user import get_user_by_email
from database import get_db
from models.user import User
from schemas.user import RefreshTokenRequest, Token

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login', response_model=Token)
@limiter.limit('5/minute')
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()],
    request : Request
):
    user = await get_user_by_email(db, form_data.username)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    access_token = create_access_token({'sub': user.email, 'type':'access'})

    refresh_token = create_refresh_token({'sub':user.email,'type':'refresh'})

    return {'access_token': access_token,
            'refresh_token': refresh_token, 
            'token_type': 'bearer'
    }


@router.post('/refresh', response_model=Token)
async def refresh_token(
    db : Annotated[AsyncSession, Depends(get_db)],
    request : RefreshTokenRequest
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= 'Invalid refresh token'
    )
        
    payload = decode_access_token(request.refresh_token)

    if payload is None:
        raise credential_exception
    
    if payload.get('type') != 'refresh':
        raise credential_exception

    email = payload.get('sub')

    if email is None:
        raise credential_exception

    user = await get_user_by_email(db, email)

    if user is None:
        raise credential_exception

    new_access_token = create_access_token({'sub':email, 'type':'access'})

    new_refresh_token = create_refresh_token({'sub': email, 'type':'refresh'})

    return {'access_token':new_access_token, 'refresh_token': new_refresh_token, 'token_type':'bearer'}

    
         

