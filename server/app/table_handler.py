import os
import json
import zipfile
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from lib.xlsx_auto import ExcelTemplateFiller
from lib.docx_auto import DocxTemplateFiller
from loguru import logger

router = APIRouter(tags=["table"])

class AutoFillingRequest(BaseModel):
    table_name: str  # 需要填充的模板文件名（如 excel-table.xlsx 或 word-table.docx）
    persons: List[str]  # 需要填充的人员ID列表

@router.post("/autofill")
def auto_filling(request: AutoFillingRequest):
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
    try:
        # 检查文件类型
        if not (request.table_name.startswith("excel") or request.table_name.startswith("word")):
            raise HTTPException(
                status_code=400,
                detail="不支持的文件类型，仅支持 excel 和 word 文件"
            )
        
        # 构建模板文件名和路径
        template_end = "xlsx" if request.table_name.startswith("excel") else "docx"
        template_name = request.table_name.split(".")[0]
        template_name = f"{template_name}-template.{template_end}"
        template_dir = "templates/xlsx" if template_end=="xlsx" else "templates/docx"
        template_path = os.path.join(template_dir, template_name)
        
        # 检查模板文件是否存在
        if not os.path.exists(template_path):
            raise HTTPException(
                status_code=404,
                detail=f"模板文件 {template_name} 不存在"
            )
        
        # 处理每个人的数据
        results = []
        for person_id in request.persons:
            try:
                # 读取个人数据
                person_data_path = f"data/persons/{person_id}.json"
                with open(person_data_path, "r", encoding="utf-8") as f:
                    person_data = json.load(f)
                
                # 构建输出文件名
                output_filename = f"{request.table_name.split('.')[0]}-{person_id}.{template_end}"
                output_path = os.path.join("static/output", output_filename)
                
                # 根据文件类型选择处理器
                if request.table_name.startswith("excel"):
                    filler = ExcelTemplateFiller(template_path, output_path)
                else:
                    filler = DocxTemplateFiller(template_path, output_path)
                    
                filler.fill(person_data)
                filler.save()
                
                results.append(output_path)
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise e
                raise HTTPException(
                    status_code=500,
                    detail=f"自动填充处理失败：{str(e)}"
                )

        if len(results) == 1:
            return {
                "status": 200,
                "message": "自动填充处理成功",
                "data": results[0]
            }
        else:
            # 创建zip文件名（使用时间戳避免重名）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_filename = f"batch_output_{timestamp}.zip"
            zip_path = os.path.join("output", zip_filename)
            
            # 创建zip文件
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for result in results:
                    file_path = os.path.join("output", result)
                    if os.path.exists(file_path):
                        # 将文件添加到zip中
                        zipf.write(file_path, result)
            
            return {
                "status": 200,
                "message": "批量处理成功，已打包为zip文件",
                "data": zip_path
            }

        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500,
            detail=f"自动填充处理失败：{str(e)}"
        )
    

    # 获取文件模板列表接口


@router.get("/list_preview")
def get_preview():
    """
    获取支持自动填表的文件模板列表。

    请求格式:
        GET /list_preview

    返回:
        status: 状态码
        message: 提示信息
        data: 文件模板名列表（List[str)）
    """
    try:
        preview_list = os.listdir("templates/preview")
        return {
            "status": 200,
            "message": "查询文件模板成功",
            "data": preview_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# 预览文件接口
@router.get("/preview/{file_name}")
def preview_file(file_name: str):
    """
    获取指定文件的预览内容（PDF），用于浏览器内嵌预览。

    参数:
        file_name: 需要预览的文件名

    请求格式:
        GET /preview/{file_name}

    返回:
        PDF 文件流（FileResponse），用于浏览器内嵌预览
    """
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
@router.get("/list_templates")
def get_templates():
    """
    超级管理员维护的模板文件，仅暴露给超级管理员查看使用

    TODO 暂未使用，后期需要添加权限控制，限制只有超级管理员可以访问此接口
    """
    try:
        word_templates = os.listdir("templates/docx")
        excel_templates = os.listdir("templates/xlsx")
        result = {
            "docx_templates": word_templates,
            "xlsx_templates": excel_templates
        }   
        return {
            "status": 200,
            "message": "查询文件模板成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))