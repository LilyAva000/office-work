import os
import json
import zipfile
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import FileResponse
from lib.xlsx_auto import ExcelTemplateFiller
from lib.docx_auto import DocxTemplateFiller
from .api_common import AppException, APIResponse, make_responses, auto_handle_exceptions
from loguru import logger
import aiofiles


router = APIRouter(tags=["table"])

class AutoFillingRequest(BaseModel):
    table_name: str
    persons: List[str]

@router.post("/autofill", response_model=APIResponse, responses=make_responses(
    'INVALID_FILE_TYPE', 'FILE_NOT_FOUND', 'AUTO_FILLING_ERROR', 'ZIP_CREATION_ERROR', 'UNKNOWN_ERROR'))
@auto_handle_exceptions
async def auto_filling(request: AutoFillingRequest):
    """
    提供对xlsx/docx表格的自动填表及下载功能。

    TODO 一次性填充多人信息待添加权限，设置管理员账号后再测试及使用

    参数:
        request: AutoFillingRequest
            - table_name: 模板文件名（如 excel-table.xlsx 或 word-table.docx）
            - persons: 需要填充的人员ID列表

    请求格式:
    ```json
    {
        "table_name": "word-table.docx",
        "persons": ["lisi"]
    },
    {
        "table_name": "excel-table.xlsx",
        "persons": ["lisi"]
    },
    {
        "table_name": "excel-table.xlsx",
        "persons": ["lisi", "zhangsan"]
    }
    ```

    返回:
        status: 状态码
        message: 提示信息
        data: 生成的文件路径（单人）或zip包路径（多人）
    """
    if not (request.table_name.startswith("excel") or request.table_name.startswith("word")):
        raise AppException(*AppException.get_error("INVALID_FILE_TYPE"))
    template_end = "xlsx" if request.table_name.startswith("excel") else "docx"
    template_name = request.table_name.split(".")[0]
    template_name = f"{template_name}-template.{template_end}"
    template_dir = "templates/xlsx" if template_end=="xlsx" else "templates/docx"
    template_path = os.path.join(template_dir, template_name)
    if not os.path.exists(template_path):
        raise AppException(*AppException.get_error("FILE_NOT_FOUND"), f"模板文件 {template_name} 不存在")
    results = []
    for person_id in request.persons:
        person_data_path = f"data/persons/{person_id}.json"
        async with aiofiles.open(person_data_path, "r", encoding="utf-8") as f:
            content = await f.read()
            person_data = json.loads(content)
        output_filename = f"{request.table_name.split('.')[0]}-{person_id}.{template_end}"
        output_path = os.path.join("static/output", output_filename)
        if request.table_name.startswith("excel"):
            filler = ExcelTemplateFiller(template_path, output_path)
        else:
            filler = DocxTemplateFiller(template_path, output_path)
        filler.fill(person_data)
        filler.save()
        results.append(output_path)
    if len(results) == 1:
        return APIResponse(code=200, msg="自动填充处理成功", data=results[0])
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"batch_output_{timestamp}.zip"
        zip_path = os.path.join("output", zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for result in results:
                file_path = os.path.join("output", result)
                if os.path.exists(file_path):
                    zipf.write(file_path, result)
        return APIResponse(code=200, msg="批量处理成功，已打包为zip文件", data=zip_path)

@router.get("/list_preview", response_model=APIResponse, responses=make_responses('UNKNOWN_ERROR'))
@auto_handle_exceptions
async def get_preview():
    """
    获取支持自动填表的文件模板列表。

    请求格式:
        GET /list_preview

    返回:
        status: 状态码
        message: 提示信息
        data: 文件模板名列表（List[str)）
    """
    preview_list = os.listdir("templates/preview")
    return APIResponse(code=200, msg="查询文件模板成功", data=preview_list)

@router.get("/preview/{file_name}", responses=make_responses('UNKNOWN_ERROR'))
@auto_handle_exceptions
async def preview_file(file_name: str):
    """
    获取指定文件的预览内容（PDF），用于浏览器内嵌预览。

    参数:
        file_name: 需要预览的文件名

    请求格式:
        GET /preview/{file_name}

    返回:
        PDF 文件流（FileResponse），用于浏览器内嵌预览
    """
    file_path = os.path.join("templates", "preview", file_name)
    if not os.path.exists(file_path):
        raise AppException(404, "文件不存在")
    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{file_name}"',
            "X-Content-Type-Options": "nosniff",
            "X-Download-Options": "noopen",
        }
    )

@router.get("/list_templates", response_model=APIResponse, responses=make_responses('UNKNOWN_ERROR'))
@auto_handle_exceptions
async def get_templates():
    """
    超级管理员维护的模板文件，仅暴露给超级管理员查看使用

    TODO 暂未使用，后期需要添加权限控制，限制只有超级管理员可以访问此接口
    """
    word_templates = os.listdir("templates/docx")
    excel_templates = os.listdir("templates/xlsx")
    result = {
        "docx_templates": word_templates,
        "xlsx_templates": excel_templates
    }
    return APIResponse(code=200, msg="查询文件模板成功", data=result)