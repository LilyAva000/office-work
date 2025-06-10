import os
import json
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from .api_common import AppException, APIResponse, make_responses, auto_handle_exceptions
from loguru import logger
import aiofiles


router = APIRouter(tags=["info"])

class PersonInfo(BaseModel):
    # 可根据实际字段补充
    person_info: dict

class CreatePersonRequest(BaseModel):
    id: str
    person: dict

class UpdatePersonRequest(BaseModel):
    person_info: dict

# 示例接口：创建基本信息
@router.post("/create_person", response_model=APIResponse, responses=make_responses('UNKNOWN_ERROR'))
@auto_handle_exceptions
async def create_info(request: CreatePersonRequest):
    person_data_path = f"data/persons/{request.id}.json"
    async with aiofiles.open(person_data_path, "w", encoding="utf-8") as file:
        await file.write(json.dumps(request.person, ensure_ascii=False))
    item = {"id": request.id, "info": request.person}
    return APIResponse(code=200, msg="创建成功", data=item)

# 示例接口：获取个人基本信息
@router.get("/{person_id}", response_model=APIResponse, responses=make_responses('PERSON_NOT_FOUND', 'UNKNOWN_ERROR'))
@auto_handle_exceptions
async def get_info(person_id: str):
    """
    获取个人基本信息
    TODO 人信息存储在 data/persons 目录下的 JSON 文件中， 后期完善要换成数据库

    参数:
        person_id: 个人唯一标识

    请求格式:
        GET /info/{person_id}

    返回:
        status: 状态码
        message: 提示信息
        data: {"person_id": person_id, "info": {个人信息字典}}
    """
    person_data_path = f"data/persons/{person_id}.json"
    try:
        async with aiofiles.open(person_data_path, "r", encoding="utf-8") as file:
            content = await file.read()
            person_info = json.loads(content)
        data = {"person_id": person_id, "info": person_info}
    except FileNotFoundError:
        raise AppException(*AppException.get_error("PERSON_NOT_FOUND"))
    return APIResponse(code=200, msg="查询成功", data=data)

# 示例接口：更新基本信息
@router.put("/{person_id}", response_model=APIResponse, responses=make_responses('UNKNOWN_ERROR'))
@auto_handle_exceptions
async def update_info(person_id: str, request: UpdatePersonRequest):
    """
    更新用户信息

    参数:
        person_id: 个人唯一标识
        person_info: 新的个人信息字典

    请求格式:
    ```json
    {
        "person_info": { ... }
    }
    ```
    返回:
        status: 状态码
        message: 提示信息
        data: {"person_id": person_id, "updated_info": person_info}
    """
    new_person_info = request.person_info
    person_data_path = f"data/persons/{person_id}.json"
    async with aiofiles.open(person_data_path, "w", encoding="utf-8") as file:
        await file.write(json.dumps(new_person_info, ensure_ascii=False))
    return APIResponse(code=200, msg="修改成功", data={"person_id": person_id, "updated_info": new_person_info})
    
# 示例接口：删除基本信息
# @router.delete("/{item_id}")
# def delete_info(item_id: str):
#     return {"message": "Item deleted successfully", "item_id": item_id}

# 上传头像接口
@router.post("/upload_avatar", response_model=APIResponse, responses=make_responses('PERSON_NOT_FOUND', 'PERSON_INFO_STRUCTURE_ERROR', 'INVALID_IMG_TYPE', 'UNKNOWN_ERROR'))
@auto_handle_exceptions
async def upload_avatar(person_id: str = Form(...), file: UploadFile = File(...)):
    """
    上传用户头像并自动更新用户信息中的照片字段。

    参数:
        person_id: 用户唯一标识ID
        file: 头像图片文件（支持常见图片格式）

    请求格式:
        multipart/form-data
        - person_id: 用户ID
        - file: 头像图片文件

    返回:
        status: 状态码
        message: 提示信息
        data: 头像图片的静态资源路径
    """
    logger.info(f"上传头像请求: person_id={person_id}, file={file.filename}")
    json_path = os.path.join("data", "persons", f"{person_id}.json")
    if not os.path.exists(json_path):
        code, msg = AppException.get_error("PERSON_NOT_FOUND")
        raise AppException(code, msg)
    async with aiofiles.open(json_path, "r", encoding="utf-8") as f:
        content = await f.read()
        data = json.loads(content)
    if not ("基本信息" in data and "个人信息" in data["基本信息"]):
        code, msg = AppException.get_error("PERSON_INFO_STRUCTURE_ERROR")
        raise AppException(code, msg)
    user_img_dir = os.path.join("static", "img", person_id)
    os.makedirs(user_img_dir, exist_ok=True)
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.gif']:
        code, msg = AppException.get_error("INVALID_IMG_TYPE")
        raise AppException(code, msg)
    avatar_filename = f"{person_id}-avatar{ext}"
    avatar_path = os.path.join(user_img_dir, avatar_filename)
    async with aiofiles.open(avatar_path, "wb") as buffer:
        content = await file.read()
        await buffer.write(content)
    avatar_url = f"static/img/{person_id}/{avatar_filename}"
    data["基本信息"]["个人信息"]["照片"] = avatar_url
    async with aiofiles.open(json_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    return APIResponse(code=200, msg="头像上传并信息更新成功", data=avatar_url)