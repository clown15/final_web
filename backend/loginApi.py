from fastapi import FastAPI
from time import time
from pydantic import BaseModel
import json
import httpx
import asyncio

app = FastAPI()

class Info(BaseModel):
    id: str
    pw: str

URL = "http://34.64.182.250:8080/login"

# ID 검증을 위한 API 호출
async def request(client, data):
    response = await client.post(URL,data=json.dumps(data))
    print(response)
    return response.text

async def task(data):
    async with httpx.AsyncClient() as client:
        tasks = request(client,data)
        result = await asyncio.gather(tasks)
        print(result)
        return result

@app.post("/login")
async def user_login(info: Info):
    """
    `login API`
    :param ID:
    :param PW:
    """
    id = info.id
    pw = info.pw
    
    result = await task({"id":info.id})

    return result
