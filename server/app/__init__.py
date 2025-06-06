from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件
from .metadata_handler import router as metadata_router
from .user_handler import router as user_router
from .table_handler import router as table_router
from utils.tools import _init_logger

# 定义tags元数据，供Swagger和Redoc分组说明
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

# 创建 FastAPI 实例，规范API文档路径和标题，禁用默认docs，redoc使用离线依赖访问/docs和/redoc
app = FastAPI(
    title="Office-Work API",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
    openapi_tags=openapi_tags
)

# 注册路由，添加API前缀
app.include_router(user_router, prefix="/api/user")
app.include_router(metadata_router, prefix="/api/info")
app.include_router(table_router, prefix="/api/table")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data/imgs", StaticFiles(directory="data/imgs"), name="imgs")

# 日志初始化
_init_logger()

# 配置跨域CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的前端源，在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

@app.get("/")
def read_root():
    """
    根路由，测试API连通性
    """
    return {"message": "Welcome to the FastAPI server!"}

# 自定义 Swagger UI 路由
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png"
    )

# 自定义 Redoc 路由，使用本地静态资源
@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>{app.title} - ReDoc</title>
    <meta charset='utf-8'/>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='/static/swagger-ui/redoc-ui.css' rel='stylesheet'>
    <link rel='shortcut icon' href='/static/swagger-ui/favicon.png'>
    <style>body {{ margin: 0; padding: 0; }}</style>
    </head>
    <body>
    <noscript>ReDoc requires Javascript to function. Please enable it to browse the documentation.</noscript>
    <redoc spec-url='{app.openapi_url}'></redoc>
    <script src='/static/swagger-ui/redoc.standalone.js'></script>
    </body>
    </html>"""
    return HTMLResponse(content=html_content, status_code=200)
