from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional

from app.core.database import db

def get_collection():
    return db.get_collection('tasks')

def create_task(title: str, description: Optional[str], priority: int) -> dict:
    task = {
        'title': title,
        'description': description,
        'completed': False,
        'priority': priority,
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }
    result = get_collection().insert_one(task)
    task['id'] = str(result.inserted_id)
    return task

def get_all_tasks() -> list:
    tasks = []
    for task in get_collection().find():
        task['id'] = str(task.pop('_id')) # _id -> id changed
        tasks.append(task)
    return tasks

def get_task_by_id(task_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(task_id):
        return None
    task = get_collection().find_one({'_id': ObjectId(task_id)})
    if task:
        task['id'] = str(task.pop('_id')) # _id -> id changed
    return task

def update_task(task_id: str, update_data: dict) -> Optional[dict]:
    if not ObjectId.is_valid(task_id):
        return None
    
    update_data = {k: v for k, v in update_data.items()if v is not None}
    
    if not update_data:
        return get_task_by_id(task_id)
    
    update_data['updated_at'] = datetime.now(timezone.utc)
    
    result = get_collection().find_one_and_update(
        {'_id': ObjectId(task_id)},
        {'$set': update_data},
        return_document=True
    )
    
    if result:
        result['id'] = str(result.pop('_id'))
    return result

def delete_task(task_id: str) -> bool:
    if not ObjectId.is_valid(task_id):
        return False
    result = get_collection().delete_one({'_id': ObjectId(task_id)})
    return result.deleted_count > 0





