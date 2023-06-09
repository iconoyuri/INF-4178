from fastapi import APIRouter
from app.globals import CHAT_SERVER_DOMAIN
from typing import List
import requests

router = APIRouter(
    prefix='/micros', tags=["Microservices"]
)


@router.get("/")
def root():
    return {"message": f"Let me try this "}

@router.get('/cserver/ping')
def ping():
    response = requests.get(f'{CHAT_SERVER_DOMAIN}/server/ping')
    return response.json()

@router.get('/server/ping')
def ping():
    return { "message": "main server - successfull ping test" }
