from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .metadata_handler import router as metadata_router
from .fileresource_handler import router as file_router

# 创建 FastAPI 实例
app = FastAPI()

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
app.mount("data/imgs", StaticFiles(directory="data/imgs"), name="imgs")
