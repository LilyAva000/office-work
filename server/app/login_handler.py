from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    valid_users = {
        "zhangsan": "password",
        "lisi": "password"
    }
    
    if request.username in valid_users and valid_users[request.username] == request.password:
        return {
            "status": "success",
            "message": "登录成功",
            "data": {"username": request.username}
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )