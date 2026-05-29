from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    email: str
    name: Optional[str]


class UserCreate(UserBase):
    password: str


class EntryBase(BaseModel):
    title: Optional[str]
    content: Optional[str]


class EntryCreate(EntryBase):
    pass


class PhotoBase(BaseModel):
    url: Optional[str]
    description: Optional[str]


class GrowthBase(BaseModel):
    title: Optional[str]
    body: Optional[str]
