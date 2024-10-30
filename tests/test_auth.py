from conftest import client, async_session_maker
from sqlalchemy import insert
from auth.models import user


async def test_add_user():
    async with async_session_maker() as session:
        stmt = insert(user).values(username="testuser",
                                   email="testuser@mail.ru",
                                   hashed_password="$2b$12$OSrN/xQ3FV8vBnlbGsScJeWjZvJ.rOMAfz.wzgzDxwr4Z2yQwIAqC",
                                   referrer_id=2,
                                   is_active=True,
                                   is_superuser=False,
                                   is_verified=False,
                                   )
        await session.execute(stmt)
        await session.commit()


def test_register():
    response = client.post("/auth/register", json={
        "email": "borisov2011@gmail.com",
        "password": "171001",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "mail"
    })
    assert response.status_code == 201


def test_email_not_verified():
    response = client.post("/auth/register", json={
        "email": "xx@xmail.om",
        "password": "171001",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "mail"
    })
    assert response.status_code == 400
