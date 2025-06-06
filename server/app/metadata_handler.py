import os
import json
import shutil
from fastapi import APIRouter, HTTPException
from fastapi import UploadFile, File, Form
from loguru import logger

router = APIRouter(tags=["info"])

# 示例接口：创建基本信息
@router.post("/create_person")
def create_info(id:str,person: dict):
    """
    TODO 暂未详细设计和使用
    """
    try:
        person_data_path = f"data/persons/{id}.json"
        with open(person_data_path, "w", encoding="utf-8") as file:
            json.dump(person, file, ensure_ascii=False)
        item = {"id": id, "info": person}
        return {
            "status": 200,
            "message": "创建成功",
            "data": {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 示例接口：获取个人基本信息
@router.get("/{person_id}")
def get_info(person_id: str):
    """
    获取个人基本信息

    参数:
        person_id: 个人唯一标识

    请求格式:
        GET /info/{person_id}

    返回:
        status: 状态码
        message: 提示信息
        data: {"person_id": person_id, "info": {个人信息字典}}
    """
    # TODO 人信息存储在 data/persons 目录下的 JSON 文件中， 后期完善要换成数据库
    person_data_path = f"data/persons/{person_id}.json" 
    try:
        with open(person_data_path, "r") as file:
            person_info = json.load(file)
        return {
            "status": 200,
            "message": "查询成功",
            "data": {"person_id": person_id, "info": person_info}
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person not found")

# 示例接口：更新基本信息
@router.put("/{person_id}")
def update_info(person_id: str, person_info: dict):
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
    try:
        new_person_info = person_info['person_info']
        person_data_path = f"data/persons/{person_id}.json"
        with open(person_data_path, "w", encoding="utf-8") as file:
            json.dump(new_person_info, file, ensure_ascii=False)
        return {
            "status": 200,
            "message": "修改成功",
            "data": {"person_id": person_id, "updated_info": person_info}
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail="Person not found")
    
# 示例接口：删除基本信息
# @router.delete("/{item_id}")
# def delete_info(item_id: str):
#     return {"message": "Item deleted successfully", "item_id": item_id}

# 上传头像接口
@router.post("/upload_avatar")
def upload_avatar(persion_id: str = Form(...), file: UploadFile = File(...) ):
    """
    上传用户头像并自动更新用户信息中的照片字段。

    参数:
        persion_id: 用户唯一标识ID
        file: 头像图片文件（支持常见图片格式）

    请求格式:
        multipart/form-data
        - persion_id: lisi
        - file: 头像图片文件

    返回:
        status: 状态码
        message: 提示信息
        avatar: 头像图片的静态资源路径
    """
    logger.info(f"上传头像请求: persion_id={persion_id}, file={file.filename}")
    try:
        # 1. 创建用户头像目录
        user_img_dir = os.path.join("static", "img", persion_id)
        os.makedirs(user_img_dir, exist_ok=True)
        # 2. 获取文件扩展名
        ext = os.path.splitext(file.filename)[1]
        avatar_filename = f"{persion_id}-avatar{ext}"
        avatar_path = os.path.join(user_img_dir, avatar_filename)
        # 3. 保存图片
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 4. 更新json文件，修改照片字段
        json_path = os.path.join("data", "persons", f"{persion_id}.json")
        if not os.path.exists(json_path):
            raise HTTPException(status_code=404, detail="用户信息文件不存在")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "基本信息" in data and "个人信息" in data["基本信息"]:
            data["基本信息"]["个人信息"]["照片"] = f"static/img/{persion_id}/{avatar_filename}"
        else:
            raise HTTPException(status_code=400, detail="用户信息结构异常")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return {"status": 200, "message": "头像上传并信息更新成功", "avatar": f"static/img/{persion_id}/{avatar_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))