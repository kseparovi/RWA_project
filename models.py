from pydantic import BaseModel, Field
from typing import Optional

class UserIn(BaseModel):
    username: str
    email: str
    password: str

class UserDb(UserIn):
    username: str = Field(alias="_id")
    email: str
    hashed_password: str

class RockSongIn(BaseModel):
    title: str
    artist: str
    album: str
    year: int

class RockSongDb(RockSongIn):
    id: str = Field(alias="_id")
