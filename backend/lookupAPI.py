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

@app.post("/lookup")
async def lookup(info: Info):
    """
    `lookup API`
    :param ID:
    """
    
    result = await task({"id":info.id})
    
    json_data = json.loads(result[0]) # string to json(dict)
    json_data["value"] = [
        {"date":"2022.08.21","info":"스타벅스","amount":"-4800","balance":"4,995,200"},
        {"date":"2022.08.20","info":"제이크","amount":"+500,000,000","balance":"500,000,000"},
        {"date":"2022.08.20","info":"제이크","amount":"+500,000,000","balance":"500,000,000"},
        {"date":"2022.08.20","info":"제이크","amount":"+500,000,000","balance":"500,000,000"},
    ]
    
    return json_data