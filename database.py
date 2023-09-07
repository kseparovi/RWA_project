from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import List
from pymongo import MongoClient
from bson import ObjectId

import models
import database

app = FastAPI()

# Povezivanje s MongoDB bazom podataka
client = MongoClient("mongodb://localhost:27017/")
db = client["rock_songs_db"]
collection = db["rock_songs"]

# Modeli za korisnike
class UserIn(models.BaseModel):
    username: str
    email: str
    password: str

class UserDb(UserIn):
    id: str

# API rute za korisnike
@app.post("/users", response_model=UserDb)
async def create_user(user: UserIn = Body(...)):
    hashed_password = security.hash_password(user.password)
    user_db = UserDb(
        id=user.username,
        email=user.email,
        password=hashed_password
    )

    new_user = await database.db["users"].insert_one(user_db.dict())
    created_user = await database.db["users"].find_one({"_id": new_user.inserted_id})
    return UserDb(**created_user)

# Modeli za rock pjesme
class RockSongIn(models.BaseModel):
    title: str
    artist: str
    album: str
    year: int

class RockSongDb(RockSongIn):
    id: str

# API rute za rock pjesme
@app.post("/songs/", response_model=RockSongDb)
async def create_song(song_in: RockSongIn):
    new_song = RockSongDb(**song_in.dict())
    result = collection.insert_one(new_song.dict())
    new_song.id = str(result.inserted_id)
    return new_song

@app.get("/songs/", response_model=List[RockSongDb])
async def read_songs():
    songs = list(collection.find())
    return songs

@app.get("/songs/{song_id}", response_model=RockSongDb)
async def read_song(song_id: str):
    song = collection.find_one({"_id": ObjectId(song_id)})
    if song:
        return RockSongDb(**song)
    else:
        raise HTTPException(status_code=404, detail="Rock song not found")

@app.delete("/songs/{song_id}", response_model=RockSongDb)
async def delete_song(song_id: str):
    song = collection.find_one({"_id": ObjectId(song_id)})
    if song:
        collection.delete_one({"_id": ObjectId(song_id)})
        return RockSongDb(**song)
    else:
        raise HTTPException(status_code=404, detail="Rock song not found")
