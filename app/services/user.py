from datetime import datetime, timezone
from typing import Optional
from pymongo import ReturnDocument

from bson import ObjectId

from app.config import db, logger
from app.config.security import get_password_hash, verify_password


def get_collection():
    return db.get_collection("users")


def get_user_by_username(username: str) -> Optional[dict]:
    user = get_collection().find_one({"username": username})
    if user:
        user["id"] = str(user.pop("_id"))
    return user


def get_user_by_email(email: str) -> Optional[dict]:
    user = get_collection().find_one({"email": email})
    if user:
        user["id"] = str(user.pop("_id"))
    return user


def create_user(username: str, email: str, password: str) -> dict:
    hashed_password = get_password_hash(password)
    user = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }
    result = get_collection().insert_one(user)
    user["id"] = str(result.inserted_id)
    user.pop("password")
    logger.info(f"User created: username={username}")
    return user


def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = get_collection().find_one({"username": username})
    if not user:
        logger.warning(f"User not found: username={username}")
        return None
    if not verify_password(password, user["password"]):
        logger.warning(f"Invalid password: username={username}")
        return None
    user["id"] = str(user.pop("_id"))
    logger.info(f"User authenticated: username={username}")
    return user
def update_user(username: str, update_data: dict) -> Optional[dict]:
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    if not update_data:
        return get_user_by_username(username)
    
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    result = get_collection().find_one_and_update(
    {"username": username},
    {"$set": update_data},
    return_document=ReturnDocument.AFTER
)
    
    if result:
        result["id"] = str(result.pop("_id"))
        result.pop("password", None)
        logger.info(f"User updated: username={username}")
    
    return result
