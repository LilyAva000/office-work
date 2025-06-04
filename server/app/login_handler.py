import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    try:
        with open("data/login/user_password.json", "r") as file:
            valid_users = json.load(file)
            
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
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="用户配置文件不存在"
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="用户配置文件格式错误"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"登录验证失败：{str(e)}"
        )