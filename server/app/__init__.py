from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse
from .metadata_handler import router as metadata_router
from .fileresource_handler import router as file_router

# 创建 FastAPI 实例，禁用默认的docs端点
app = FastAPI(docs_url=None, redoc_url=None)

# 示例接口：根路径
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

# 示例接口：获取用户信息
@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "info": "This is a placeholder for user information."}

# 注册路由
app.include_router(metadata_router)
app.include_router(file_router)

# 暴露 static 目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 暴露 data/imgs 目录
app.mount("/data/imgs", StaticFiles(directory="data/imgs"), name="imgs")

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

# 自定义 OpenAPI 路由
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(title="API", version="1.0.0", routes=app.routes)
