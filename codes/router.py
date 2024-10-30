from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from redis_config import get_redis

from database import get_async_session
from codes.models import referral_code
from codes.schemas import CodeCreate
from auth.base_config import auth_backend
from auth.models import User
from auth.manager import get_user_manager

from fastapi_users import FastAPIUsers

from codes.services import generate_random_code, calculate_expiration_date

router = APIRouter(
    prefix="/codes",
    tags=["Codes"]
)

fastapi_user = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_user.current_user()


@router.get("/get")
async def get_code(email: str,
                   session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(referral_code.c.code).select_from(
            referral_code.join(User, referral_code.c.user_id == User.id)).where(User.email == email)
        result = await session.execute(stmt)
        code = result.fetchone()[0]
        return code
    except Exception:
        raise HTTPException(status_code=404,
                            detail=f"Реферальный код для {email} не найден.")


@router.post("/add")
async def add_code(session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    try:
        existing_code = await session.execute(select(referral_code).where(
            referral_code.c.user_id == user.id).limit(1))
        existing_code = existing_code.fetchone()

        if existing_code:
            raise HTTPException(status_code=400, detail="У вас уже есть реферальный код.")

        new_code = CodeCreate()

        new_code.code = generate_random_code()
        new_code.expiration_date = calculate_expiration_date()

        stmt_referral_code = insert(referral_code).values(**new_code.dict(), user_id=user.id)
        await session.execute(stmt_referral_code)
        await session.commit()

        redis = await get_redis()
        await redis.set(f"user:{user.id}:referral_code", new_code.code, ex=60 * 60 * 24)

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add code: {str(e)}")
    formatted_expiration_date = new_code.expiration_date.strftime("%d-%m-%Y %H:%M")

    return {"Ваш реферальный код": new_code.code, "Срок действия": formatted_expiration_date}


@router.delete("/delete")
async def delete_code(session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    stmt = delete(referral_code).where(referral_code.c.user_id == User.id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "Реферальный код успешно удален"}
