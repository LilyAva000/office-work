import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

# 示例接口：获取个人基本信息
@router.get("/info/{person_id}")
def get_info(person_id: str):
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

# 示例接口：创建基本信息
@router.post("/info/create_person")
def create_info(id:str,person: dict):
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

# 示例接口：更新基本信息
@router.put("/info/{person_id}")
def update_info(person_id: str, person_info: dict):
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
# @router.delete("/info/{item_id}")
# def delete_info(item_id: str):
#     return {"message": "Item deleted successfully", "item_id": item_id}
