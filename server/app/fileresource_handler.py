import os
import shutil
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Form


router = APIRouter()

# 文件上传接口
# @router.post("/upload")
# def upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename, "message": "File uploaded successfully"}

import os.path
from fastapi.responses import FileResponse, Response

# 文件下载接口
@router.get("/download/{file_name}")
def download_file(file_name: str):
    try:
        # TODO 改为下载已填好的表，需修改代码
        file_path = os.path.join("templates", "preview", file_name)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"文件 {file_name} 不存在"
            )
        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/octet-stream"
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"下载文件时发生错误：{str(e)}"
        )

# 预览文件接口
@router.get("/preview/{file_name}")
def preview_file(file_name: str):
    try:
        file_path = os.path.join("templates", "preview", file_name)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail=f"文件 {file_name} 不存在"
            )

        return FileResponse(
            path=file_path,
            filename=file_name,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="{file_name}"',
                "X-Content-Type-Options": "nosniff",  # 防止猜测 MIME
                "X-Download-Options": "noopen",       # 防止触发下载
            }
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"预览文件时发生错误：{str(e)}"
        )

# 获取文件模板列表接口
@router.get("/list_preview")
def get_preview():
    try:
        preview_list = os.listdir("templates/preview")
        return {
            "status": 200,
            "message": "查询文件模板成功",
            "data": preview_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 获取文件模板列表接口
@router.get("/list_templates")
def get_templates():
    try:
        word_templates = os.listdir("templates/word")
        excel_templates = os.listdir("templates/excel")
        result = {
            "word_templates": word_templates,
            "excel_templates": excel_templates
        }   
        return {
            "status": 200,
            "message": "查询文件模板成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 上传头像接口
@router.post("/upload_avatar")
def upload_avatar(username: str = Form(...), file: UploadFile = File(...) ):
    try:
        # 1. 创建用户头像目录
        user_img_dir = os.path.join("static", "img", username)
        os.makedirs(user_img_dir, exist_ok=True)
        # 2. 获取文件扩展名
        ext = os.path.splitext(file.filename)[1]
        avatar_filename = f"{username}-avatar{ext}"
        avatar_path = os.path.join(user_img_dir, avatar_filename)
        # 3. 保存图片
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 4. 更新json文件，修改照片字段
        json_path = os.path.join("data", "persons", f"{username}.json")
        if not os.path.exists(json_path):
            raise HTTPException(status_code=404, detail="用户信息文件不存在")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "基本信息" in data and "个人信息" in data["基本信息"]:
            data["基本信息"]["个人信息"]["照片"] = f"static/img/{username}/{avatar_filename}"
        else:
            raise HTTPException(status_code=400, detail="用户信息结构异常")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return {"status": 200, "message": "头像上传并信息更新成功", "avatar": f"static/img/{username}/{avatar_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))