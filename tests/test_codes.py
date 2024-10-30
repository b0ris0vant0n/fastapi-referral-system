from conftest import client, async_session_maker
from sqlalchemy import insert, select
from codes.models import referral_code
from datetime import datetime


async def test_add_code():
    async with async_session_maker() as session:
        stmt = insert(referral_code).values(id=1,
                                            user_id=1,
                                            code="jdkJsjjhdkll",
                                            expiration_date=datetime(2024, 3, 23, 18, 56, 13, 889344)
                                            )
        await session.execute(stmt)
        await session.commit()

        query = select(referral_code)
        result = await session.execute(query)
        assert result.all() == [(1, 1, 'jdkJsjjhdkll', datetime(2024, 3, 23, 18, 56, 13, 889344))]


def test_get_code():
    response = client.get("/codes/get", params={
        "email": "testuser@mail.ru",
    })
    assert response.status_code == 200
