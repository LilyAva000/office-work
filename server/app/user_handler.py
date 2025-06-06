import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from loguru import logger

router = APIRouter(tags=["user"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    """
    用户登录接口

    参数:
        request: LoginRequest
            - username: 用户名
            - password: 密码

    请求格式:
    ```json
    {
        "username": "lisi",
        "password": "123456"
    }
    ```

    TODO 后期完善登录验证功能，需要返回用户唯一标识ID供前端全局存储使用
    返回:
        status: 状态码
        message: 提示信息
        data: {"username": 用户名}
    """
    try:
        with open("data/login/user_password.json", "r") as file:
            valid_users = json.load(file)
            
        if request.username in valid_users and valid_users[request.username] == request.password:
            return {
                "status": 200,
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