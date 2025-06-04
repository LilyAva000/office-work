import json
from fastapi import APIRouter

router = APIRouter()

# 示例接口：获取个人基本信息
@router.get("/info/{person_id}")
def get_info(person_id: str):
    person_data_path = f"data/persons/{person_id}.json"
    try:
        with open(person_data_path, "r") as file:
            person_info = json.load(file)
        return {"person_id": person_id, "info": person_info}
    except FileNotFoundError:
        return {"error": "Person not found"}, 404

# 示例接口：创建基本信息
@router.post("/info/create_person")
def create_info(id:str,person: dict):
    try:
        person_data_path = f"data/persons/{id}.json"
        with open(person_data_path, "w") as file:
            json.dump(person, file)
        item = {"id": id, "info": person}
        return {"message": "Person created successfully", "item": item}
    except Exception as e:
        return {"error": str(e)}, 500

# 示例接口：更新基本信息
@router.put("/info/{item_id}")
def update_info(item_id: int, item: dict):
    try:
        person_data_path = f"data/persons/{item_id}.json"
        with open(person_data_path, "w") as file:
            json.dump(item, file)
        return {"message": "Item updated successfully", "item_id": item_id, "item": item}
    except FileNotFoundError:
        return {"error": "Person not found"}, 404
    
# 示例接口：删除基本信息
@router.delete("/info/{item_id}")
def delete_info(item_id: str):
    return {"message": "Item deleted successfully", "item_id": item_id}
