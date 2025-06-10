from fastapi import FastAPI
from .startup import setup_app
from utils.tools import _init_logger

openapi_tags = [
    {
        "name": "user",
        "description": "用户相关接口，包括登录验证等操作。TODO 后期要完善权限设置和用户管理功能。"
    },
    {
        "name": "info",
        "description": "个人信息相关接口，包括查询、更新、创建等操作。"
    },
    {
        "name": "table",
        "description": "表格相关接口，支持xlsx/docx模板的自动填表、批量下载等功能。"
    }
]

app = FastAPI(
    title="Office-Work API",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    openapi_tags=openapi_tags
)

setup_app(app)


# 日志初始化
_init_logger()
