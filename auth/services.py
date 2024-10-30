from sqlalchemy import select
from datetime import datetime

from codes.models import referral_code
import httpx
from fastapi import HTTPException
from config import EMAIL_API_KEY


async def get_user_by_referral_code(referral_code_str: str,
                                    session) -> int:
    query = select(referral_code).where(referral_code.c.code == referral_code_str)
    referral_code_entry = await session.execute(query)
    referral_code_obj = referral_code_entry.fetchone()

    if referral_code_obj is None:
        raise HTTPException(status_code=404, detail="Реферальный код не найден")

    if referral_code_obj.expiration_date < datetime.now():
        raise HTTPException(status_code=400, detail="Реферальный код истек")

    return referral_code_obj.user_id


async def verify_email(email):
    url = f"https://api.hunter.io/v2/email-verifier"
    params = {"email": email, "api_key": EMAIL_API_KEY}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['data']['result'] != "deliverable":
            raise HTTPException(status_code=400, detail="Неверный адрес электронной почты")
        return True
    else:
        raise HTTPException(status_code=500, detail="Ошибка при проверке электронной почты")
