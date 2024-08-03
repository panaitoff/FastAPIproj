from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# MongoDB setup
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.messages
message_collection = database.get_collection("messages")

class Message(BaseModel):
    content: str

@app.get("/api/v1/messages/")
async def get_messages():
    messages = []
    async for message in message_collection.find():
        messages.append(message)
    return messages

@app.post("/api/v1/message/")
async def create_message(message: Message):
    new_message = await message_collection.insert_one(message.dict())
    created_message = await message_collection.find_one({"_id": new_message.inserted_id})
    return created_message