from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional

from app.config import db, logger

def get_collection():
    return db.get_collection('tasks')

def create_task(title: str, description: Optional[str], priority: int, user_id: str) -> dict:
    task = {
        'title': title,
        'description': description,
        'completed': False,
        'priority': priority,
        'user_id': user_id,
        'created_at': datetime.now(timezone.utc),
        'updated_at': datetime.now(timezone.utc)
    }
    result = get_collection().insert_one(task)
    task['id'] = str(result.inserted_id)
    logger.info(f"Task created: id={task['id']}, user={user_id}")
    return task

def get_all_tasks(user_id: str, skip: int = 0, limit: int = 20) -> list:
    tasks = []
    cursor = get_collection().find({'user_id': user_id}).skip(skip).limit(limit)
    for task in cursor:
        task['id'] = str(task.pop('_id'))
        tasks.append(task)
    return tasks

def get_task_by_id(task_id: str, user_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(task_id):
        logger.warning(f"Invalid task id: {task_id}")
        return None
    task = get_collection().find_one({'_id': ObjectId(task_id), 'user_id': user_id})
    if task:
        task['id'] = str(task.pop('_id'))
        logger.info(f"Task retrieved: id={task_id}")
    else:
        logger.warning(f"Task not found: id={task_id}")
    return task

def update_task(task_id: str, user_id: str, update_data: dict) -> Optional[dict]:
    if not ObjectId.is_valid(task_id):
        logger.warning(f"Invalid task id: {task_id}")
        return None

    update_data = {k: v for k, v in update_data.items() if v is not None}

    if not update_data:
        return get_task_by_id(task_id, user_id)

    update_data['updated_at'] = datetime.now(timezone.utc)

    result = get_collection().find_one_and_update(
        {'_id': ObjectId(task_id), 'user_id': user_id},
        {'$set': update_data},
        return_document=True
    )

    if result:
        result['id'] = str(result.pop('_id'))
        logger.info(f"Task updated: id={task_id}")
    else:
        logger.warning(f"Task not found for update: id={task_id}")
    return result

def delete_task(task_id: str, user_id: str) -> bool:
    if not ObjectId.is_valid(task_id):
        logger.warning(f"Invalid task id: {task_id}")
        return False
    result = get_collection().delete_one({'_id': ObjectId(task_id), 'user_id': user_id})
    if result.deleted_count > 0:
        logger.info(f"Task deleted: id={task_id}")
        return True
    else:
        logger.warning(f"Task not found for delete: id={task_id}")
        return False
