from typing import Optional
from urllib import response

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class Info(BaseModel):
    id: str

class Response(BaseModel):
    message: str = None

@app.post("/login")
def user_login(info: Info):
    """
    `login API`
    :param ID:
    :param PW:
    """
    response = Response()

    if info.id != "testid" :
        response.message = "OK"
    else:
        response.message = "ID Error"

    return response

@app.get("/login")
def test_login():
    data = {
        "id":"id",
        "pw":"password"
    }
    return data

@app.get("/")
def read_root():
    return {"Hello": "World"}