from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.models.users import User

# Configurações de segurança
SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutos
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 dias

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict) -> str:
    """
    Cria um Access Token com curta duração (30 minutos).

    Args:
        data: Dicionário com os dados a serem incluídos no token (ex: {'sub': email})

    Returns:
        Token JWT codificado como string
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire, 'type': 'access'})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Cria um Refresh Token com longa duração (7 dias).

    Args:
        data: Dicionário com os dados a serem incluídos no token (ex: {'sub': email})

    Returns:
        Token JWT codificado como string
    """
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({'exp': expire, 'type': 'refresh'})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = 'access') -> dict:
    """
    Verifica e decodifica um token JWT.

    Args:
        token: Token JWT a ser verificado
        token_type: Tipo esperado do token ('access' ou 'refresh')

    Returns:
        Payload decodificado do token

    Raises:
        HTTPException: Se o token for inválido, expirado ou do tipo errado
    """
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verifica se o tipo do token está correto
        if payload.get('type') != token_type:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f'Token inválido: esperado tipo {token_type}',
                headers={'WWW-Authenticate': 'Bearer'},
            )

        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token expirado',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except DecodeError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token inválido ou malformado',
            headers={'WWW-Authenticate': 'Bearer'},
        )


def get_password_hash(password: str) -> str:
    """
    Gera hash de senha usando Argon2.

    Args:
        password: Senha em texto plano

    Returns:
        Hash da senha
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha corresponde ao hash.

    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash da senha armazenado

    Returns:
        True se a senha corresponder, False caso contrário
    """
    return pwd_context.verify(plain_password, hashed_password)


# OAuth2 scheme para extração do token do header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Dependency para validar Access Token e retornar o usuário autenticado.

    Args:
        session: Sessão do banco de dados
        token: Access Token extraído do header Authorization

    Returns:
        Objeto User autenticado

    Raises:
        HTTPException: Se o token for inválido ou o usuário não existir
    """
    # Verifica e decodifica o Access Token
    payload = verify_token(token, token_type='access')

    # Extrai o email do subject
    subject_email = payload.get('sub')
    if not subject_email:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Token inválido: subject não encontrado',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    # Busca o usuário no banco de dados
    user = session.scalar(select(User).where(User.email == subject_email))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Usuário não encontrado',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user
