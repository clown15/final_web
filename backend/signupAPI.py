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
    
    if json_data['message'] == "OK":
        if info.pw != info.re_pw:
            json_data['message'] = "비밀번호가 서로 다릅니다."
    else:
        json_data['message'] = "ID가 중복되었습니다."
    
    return json_data