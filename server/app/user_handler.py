import json
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from loguru import logger
from lib.error_response import get_error

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
            status, message = 200, "登录成功"
            data = {"username": request.username}
            return {"status":status, "message":message,"data":data}
        else:
            status, message = get_error("INVALID_AUTHORIZATION")
            return {"status":status, "message":message,"data":None}
    except FileNotFoundError:
        status, message = get_error("DATABASE_ERROR")
        return {"status":status, "message":message,"data":"服务器没有账密数据"}
    except json.JSONDecodeError:
        status, message = get_error("USER_CONFIG_FILE_FORMAT_ERROR")
        return {"status":status, "message":message,"data":None}
    except Exception as e:
        status, message = get_error("UNKNOWN_ERROR")
        return {"status":status, "message":message,"data":f"登录验证失败：{str(e)}"}
