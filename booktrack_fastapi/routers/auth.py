from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
from booktrack_fastapi.models.users import User
from booktrack_fastapi.schemas.users import TokenResponse

router = APIRouter(prefix='/auth', tags=['Authentication'])

oauth2_scheme_refresh = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post('/token', response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretos',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Email ou senha incorretos',
        )
    token_data = {'sub': user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


@router.post('/refresh', response_model=TokenResponse)
async def refresh_access_token(
    token: str = Depends(oauth2_scheme_refresh),
    session: AsyncSession = Depends(get_session),
):
    payload = verify_token(token, token_type='refresh')
    subject_email = payload.get('sub')
    if not subject_email:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token inválido: subject não encontrado',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user = await session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Usuário não encontrado',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    token_data = {'sub': user.email}
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token,
        'token_type': 'bearer',
    }
