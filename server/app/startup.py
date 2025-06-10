from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .metadata_handler import router as metadata_router
from .user_handler import router as user_router
from .table_handler import router as table_router
from .api_common import register_exception_handlers
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.responses import HTMLResponse

def setup_app(app):
    # 注册路由
    app.include_router(user_router, prefix="/api/user")
    app.include_router(metadata_router, prefix="/api/info")
    app.include_router(table_router, prefix="/api/table")

    # 挂载静态文件
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/data/imgs", StaticFiles(directory="data/imgs"), name="imgs")

    # 注册全局异常处理
    register_exception_handlers(app)

    # 配置跨域CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 其它自定义基础路由
    @app.get("/")
    def read_root():
        """
        根路由，测试API连通性
        """
        return {"message": "Welcome to the FastAPI server!"}

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui/swagger-ui.css",
            swagger_favicon_url="/static/swagger-ui/favicon.png"
        )

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
