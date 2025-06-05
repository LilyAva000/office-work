import os
import json
import zipfile
from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from lib.xlsx_auto import ExcelTemplateFiller

router = APIRouter()

class AutoFillingRequest(BaseModel):
    table_name: str
    persons: List[str]

@router.post("/filling/autofilling")
def auto_filling(request: AutoFillingRequest):
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
        template_dir = "templates/excel" if template_end=="xlsx" else "templates/word"
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
                with open(person_data_path, "r") as f:
                    person_data = json.load(f)
                
                # 构建输出文件名
                output_filename = f"{request.table_name.split('.')[0]}-{person_id}.{template_end}"
                output_path = os.path.join("output", output_filename)
                
                # 根据文件类型选择处理器
                if request.table_name.startswith("excel"):
                    filler = ExcelTemplateFiller(template_path, output_path)
                    filler.fill(person_data)
                    filler.save()
                else:
                    doc = DocxTemplate(template_path)
                    try:
                        person_data['照片'] = InlineImage(doc, info['照片'], height=Mm(35))
                    except:
                        None
                    doc.render(person_data)
                    doc.save(output_path)
                
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