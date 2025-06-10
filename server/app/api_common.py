# =====================
# 响应模型 & 错误码加载
# =====================
import yaml
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from typing import Any, Optional
from functools import wraps
import inspect

# 只加载一次错误码配置
def _load_errors() -> dict:
    return yaml.safe_load(Path("config/error_config.yaml").read_text(encoding="utf-8"))

ERRORS = _load_errors()

class APIResponse(BaseModel):
    code: int
    msg: str
    data: Optional[Any] = None

    #  Pydantic 的标准用法。Config 里的 schema_extra 可以为该模型自动生成 OpenAPI 文档时, 提供示例（example）
    class Config:
        schema_extra = {
            "example": {
                "code": 200,
                "msg": "操作成功",
                "data": {"some": "value"}
            }
        }

# =====================
# 业务异常
# =====================
class AppException(Exception):
    def __init__(self, code: int, msg: str, data: any = None):
        self.code = code
        self.msg = msg
        self.data = data
    
    @staticmethod
    def get_error(key: str) -> tuple[int, str]:
        err = ERRORS.get(key)
        if not err:
            return 500, f"Unknown error key: {key}"
        return err["code"], err["message"]

# =====================
# 工具函数
# =====================
def make_responses(*error_keys: str) -> dict:
    """
    根据 error_config.yaml 的key列表, 自动生成FastAPI接口装饰器的responses参数, 包含description和example。
    用法: responses=make_responses('INVALID_FILE_TYPE', 'FILE_NOT_FOUND', ...)
    """
    responses = {}
    for key in error_keys:
        err = ERRORS.get(key)
        if not err:
            continue
        code = err['code']
        msg = err['message']
        responses[code] = {
            "description": msg,
            "content": {
                "application/json": {
                    "example": {
                        "code": code,
                        "msg": msg,
                        "data": "" if code != 500 else "错误详情"
                    }
                }
            }
        }
    return responses

def auto_handle_exceptions(func) -> callable:
    """
    装饰器: 自动捕获并处理 AppException/Exception, 统一接口异常响应, 减少重复 try/except。
    用法: @auto_handle_exceptions
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except AppException as e:
            raise e
        except Exception as e:
            code, msg = AppException.get_error("UNKNOWN_ERROR")
            raise AppException(code, msg, str(e))
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AppException as e:
            raise e
        except Exception as e:
            code, msg = AppException.get_error("UNKNOWN_ERROR")
            raise AppException(code, msg, str(e))
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# =====================
# 全局异常处理注册
# =====================
def register_exception_handlers(app) -> None:
    """FastAPI 全局异常处理器: 
    - app_exception_handler: 自定义AppException, 处理业务异常, 如参数错误、权限不足等。
    - http_exception_handler: 处理 HTTP 异常, 如 404、405 等。
    - validation_exception_handler: 处理参数校验失败, 如类型错误、格式不符。
    - global_exception_handler: 兜底处理其他未捕获异常, 如代码 bug、系统异常等。
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(request, exc: AppException):
        # 业务异常, 始终带data字段
        return JSONResponse(
            status_code=exc.code if exc.code else 500,
            content=APIResponse(code=exc.code, msg=exc.msg, data=exc.data if exc.data is not None else None).dict()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc: StarletteHTTPException):
        code, msg = AppException.get_error("UNKNOWN_ERROR")
        detail = exc.detail
        if isinstance(detail, dict):
            code = detail.get("code", code)
            msg = detail.get("msg", msg)
        elif isinstance(detail, str):
            msg = detail
        # 其它HTTP异常, data为None
        return JSONResponse(status_code=code, content=APIResponse(code=code, msg=msg, data=None).dict())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        code, msg = AppException.get_error("PARAMETERS_ERROR")
        # 校验异常, data为详细错误
        return JSONResponse(
            status_code=code,
            content=APIResponse(code=code, msg=msg, data=exc.errors()).dict()
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc: Exception):
        # 捕获所有未处理异常, 500, data为详细错误
        code, msg = AppException.get_error("UNKNOWN_ERROR")
        return JSONResponse(
            status_code=500,
            content=APIResponse(code=500, msg=msg, data=str(exc)).dict()
        )
