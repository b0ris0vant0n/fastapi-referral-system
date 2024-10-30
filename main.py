from fastapi_users import FastAPIUsers
from fastapi import FastAPI
from contextlib import asynccontextmanager

from redis_config import get_redis, close_redis

from auth.base_config import auth_backend
from auth.models import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from codes.router import router as router_codes
from referral.router import router as referral

@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_redis()
    yield
    await close_redis()

app = FastAPI(
    title="Referral Codes App",
    lifespan=lifespan
)

fastapi_user = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_user.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authorization"],
)

app.include_router(
    fastapi_user.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authorization"],
)

current_user = fastapi_user.current_user()


app.include_router(router_codes)
app.include_router(referral)
