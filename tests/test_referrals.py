from conftest import client, async_session_maker
from sqlalchemy import insert
from auth.models import user


async def test_add_referral():
    async with async_session_maker() as session:
        stmt = insert(user).values(username="testuser2",
                                   email="testuser2@mail.ru",
                                   hashed_password="$2b$12$OSrN/xQ3FV8vBnlbGsScJeWjZvJ.rOMAfz.wzgzDxwr4Z2yQwIAqC",
                                   referrer_id=2,
                                   is_active=True,
                                   is_superuser=False,
                                   is_verified=False,
                                   )
        await session.execute(stmt)
        await session.commit()


def test_get_referral():
    response = client.get(f"/referrals/{2}")
    assert response.status_code == 200
