from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import httpx
import asyncio

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Info(BaseModel):
    id: str
    pw: str
    re_pw: str

class Message(BaseModel):
    message: str = None

async def request(client, data):
    URL = "http://34.64.182.250:8080/login"
    response = await client.post(URL,data=json.dumps(data))
    
    return response.text

async def task(data):
    async with httpx.AsyncClient() as client:
        tasks = request(client,data)
        result = await asyncio.gather(tasks)
    
        return result

@app.post("/signup")
async def signup(info: Info):
    """
    `signup API`
    :param ID:
    :param PW:
    :param rePW:
    """
    
    result = await task({"id":info.id})
    
    json_data = json.loads(result[0])
    
    message = Message()
    if json_data['message'] != "Error":
        if info.pw != info.re_pw:
            message.message = "password Error"
            
            return message.__dict__
    else:
        message.message = "ID Error"
        return message.__dict__
    
    return json.loads(result[0])