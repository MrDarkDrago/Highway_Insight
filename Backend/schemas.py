from pydantic import BaseModel
from typing import Optional

class CityName(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy conversion to Pydantic



class UserCreate(BaseModel):
    username: str
    email: str
    password: str
