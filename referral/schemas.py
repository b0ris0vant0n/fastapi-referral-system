from pydantic import BaseModel


class Referral(BaseModel):
    id: int
    email: str
    username: str
