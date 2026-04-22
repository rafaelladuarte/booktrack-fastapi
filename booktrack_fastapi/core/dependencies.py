from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booktrack_fastapi.core.database import get_session
from booktrack_fastapi.core.security import get_current_user
from booktrack_fastapi.models.users import User, UserRole

SessionDep = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    """
    Dependency que garante que o usuário atual tem papel de admin.

    Args:
        user: Usuário autenticado obtido via get_current_user

    Returns:
        O usuário se for admin

    Raises:
        HTTPException: 403 Forbidden se o usuário não for admin
    """
    if user.role != UserRole.admin.value:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Acesso negado: privilégios de administrador necessários',
        )
    return user


AdminUser = Annotated[User, Depends(require_admin)]
