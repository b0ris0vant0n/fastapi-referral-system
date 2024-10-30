from typing import Optional

from fastapi import Depends, Request, HTTPException
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models
from sqlalchemy.exc import IntegrityError
from fastapi_users import exceptions as fastapi_users_exceptions

from auth.models import User
from auth.utils import get_user_db
from database import get_async_session
from auth.schemas import UserCreate
from auth.services import get_user_by_referral_code, verify_email
from sqlalchemy.ext.asyncio import AsyncSession
from config import SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    def __init__(self, user_db, session: AsyncSession):
        super().__init__(user_db)
        self.session = session

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: UserCreate,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)
        session = self.session

        referrer = None

        if user_create.referral_code_str:
            referrer = await get_user_by_referral_code(user_create.referral_code_str, session)
            if not referrer:
                raise HTTPException(status_code=400, detail="Недействительный реферальный код")

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        await verify_email(user_create.email)

        user_dict = user_create.dict(exclude={"referral_code_str"})
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        if referrer:
            user_dict["referrer_id"] = referrer

        user_dict["is_active"] = user_create.is_active
        user_dict["is_superuser"] = user_create.is_superuser
        user_dict["is_verified"] = user_create.is_verified
        try:
            created_user = await self.user_db.create(user_dict)
        except IntegrityError as e:
            await session.rollback()
            if 'Key (username)' in str(e.orig):
                raise HTTPException(status_code=400, detail="Такой username уже используется")
            else:
                raise fastapi_users_exceptions.UserAlreadyExists()

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(
    user_db=Depends(get_user_db),
    session: AsyncSession = Depends(get_async_session)
):
    yield UserManager(user_db, session=session)
