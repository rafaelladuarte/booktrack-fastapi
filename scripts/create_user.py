# ruff: noqa: E501, PLR2004
import argparse
import asyncio
import re
import sys

from sqlalchemy import select

from booktrack_fastapi.core.database import async_session_maker
from booktrack_fastapi.core.security import get_password_hash
from booktrack_fastapi.models.users import User

EMAIL_REGEX = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


async def create_user(email: str, password: str, role: str):
    if not EMAIL_REGEX.match(email):
        print(f"Erro: O e-mail '{email}' não tem um formato válido.")
        sys.exit(1)

    if len(password) < 8:
        print('Erro: A senha deve ter no mínimo 8 caracteres.')
        sys.exit(1)

    try:
        async with async_session_maker() as session:
            stmt = select(User).where(User.email == email)
            existing_user = await session.scalar(stmt)

            if existing_user:
                print(f"Erro: Já existe um usuário cadastrado com o e-mail '{email}'.")
                sys.exit(1)

            hashed_password = get_password_hash(password)

            new_user = User(username=email, email=email, password=hashed_password, role=role)
            session.add(new_user)
            await session.commit()

            print(f"Sucesso: Usuário '{email}' ({role}) cadastrado com exito!")
            sys.exit(0)

    except SystemExit:
        raise
    except Exception as e:
        print(f'Erro inesperado de banco de dados: {e}')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Cadastra um novo usuário no banco de dados.')
    parser.add_argument('--email', required=True, help='E-mail do usuário (usado para login)')
    parser.add_argument(
        '--password', required=True, help='Senha segura correspondente (min. 8 caracteres)'
    )
    parser.add_argument(
        '--role',
        required=False,
        help='Role do usuário',
        choices=['admin', 'viewer'],
        default='viewer',
    )
    args = parser.parse_args()

    asyncio.run(create_user(args.email, args.password, args.role))


if __name__ == '__main__':
    main()
