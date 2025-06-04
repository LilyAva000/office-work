import os
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

# 文件上传接口
@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "message": "File uploaded successfully"}

# 文件下载接口
@router.get("/download/{file_name}")
def download_file(file_name: str):
    return {"file_name": file_name, "message": "This is a placeholder for file download functionality."}

# 获取文件模板列表接口
@router.get("/list_empty")
def get_empty():
    emptys = os.listdir("templates/empty")
    return {"message": "获取空模板列表成功", "data": emptys}

# 获取文件模板列表接口
@router.get("/list_templates")
def get_templates():
    word_templates = os.listdir("templates/word")
    excel_templates = os.listdir("templates/excel")
    result = {
        "word_templates": word_templates,
        "excel_templates": excel_templates
    }
    return result