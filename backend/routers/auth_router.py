from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.dependencies import get_api_key

auth_router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/register")
def register(data: RegisterRequest, api_key: str = Depends(get_api_key)):
    return {"username": data.username, "email": data.email}

@auth_router.post("/login")
def login(data: LoginRequest, api_key: str = Depends(get_api_key)):
    return {"username": data.username, "status": "logged in"}
