from pydantic import BaseModel, Field
from datetime import datetime


class CodeCreate(BaseModel):
    code: str = Field(None, alias="code")
    expiration_date: datetime = Field(None, alias="expiration_date")
