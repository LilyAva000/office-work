import os
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

# 文件上传接口
# @router.post("/upload")
# def upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename, "message": "File uploaded successfully"}

import os.path
from fastapi.responses import FileResponse

# 文件下载接口
@router.get("/download/{file_name}")
def download_file(file_name: str):
    try:
        file_path = os.path.join("templates", "empty", file_name)
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

# 获取文件模板列表接口
@router.get("/list_empty")
def get_empty():
    try:
        emptys = os.listdir("templates/empty")
        return {
            "status": 200,
            "message": "查询文件模板成功",
            "data": emptys
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