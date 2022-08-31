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

URL = "http://34.64.182.250:8080/login"

# ID 검증을 위한 API 호출
async def request(client, data):
    response = await client.post(URL,data=json.dumps(data))
    
    return response.text

async def task(data):
    async with httpx.AsyncClient() as client:
        tasks = request(client,data)
        result = await asyncio.gather(tasks)
    
        return result

@app.post("/login")
async def user_login(info: Info):
    """
    `login API`
    :param ID:
    :param PW:
    """
    
    result = await task({"id":info.id})
    
    json_data = json.loads(result[0])
    if json_data['message'] != "OK":
        json_data['message']="아이디 또는 비밀번호가 틀렸습니다."

    return json_data
