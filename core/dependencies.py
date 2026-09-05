from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token
from crud.user import get_user_by_email
from database import get_db
from models.user import User

oauth2chema = OAuth2PasswordBearer(tokenUrl='/auth/login')

async def get_current_user(
        token : Annotated[str, Depends(oauth2chema)],
        db : Annotated[AsyncSession, Depends(get_db)]
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= 'Could not validate credentials',
        headers= {'WWW-Authenticate': 'Bearer'}
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credential_exception

    token_type = payload.get('type')

    if token_type != 'access':
        raise credential_exception

    email = payload.get('sub')

    if email is None:
        raise credential_exception

    user = await get_user_by_email(db, email)

    if user is None:
        raise credential_exception

    return user