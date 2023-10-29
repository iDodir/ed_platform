from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        email: EmailStr,
        hashed_password: str,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        query = (
            update(User)
            .where(User.user_id == user_id, User.is_active == True)
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        return res.scalar()

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        return res.scalar()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        return res.scalar()

    async def update_user(self, user_id: UUID, **kwargs) -> Optional[UUID]:
        query = (
            update(User)
            # .where(User.user_id == user_id, User.is_active == True)
            .where(User.user_id == user_id)
            .values(**kwargs)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        return res.scalar()
