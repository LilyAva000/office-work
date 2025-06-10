import json
from pydantic import BaseModel
from fastapi import APIRouter
from .api_common import AppException, APIResponse, make_responses, auto_handle_exceptions
from loguru import logger
import aiofiles

router = APIRouter(tags=["user"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=APIResponse, responses=make_responses('INVALID_AUTHORIZATION', 'USER_CONFIG_FILE_FORMAT_ERROR', 'DATABASE_ERROR', 'UNKNOWN_ERROR'))
@auto_handle_exceptions
async def login(request: LoginRequest):
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
    async with aiofiles.open("data/login/user_password.json", "r") as file:
        content = await file.read()
        valid_users = json.loads(content)
    if request.username in valid_users and valid_users[request.username] == request.password:
        return APIResponse(code=200, msg="登录成功", data={"username": request.username})
    else:
        logger.warning(f"登录失败: 用户名={request.username}")
        code, msg = AppException.get_error("INVALID_AUTHORIZATION")
        raise AppException(code, msg)
