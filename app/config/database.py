from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.config.config import settings

class MongoDB:
    def __init__(self):
        self.client: MongoClient = None
        self.database: Database = None
        
    def connect(self):
        self.client = MongoClient(settings.mongo_uri)
        self.database = self.client[settings.database_name]
        self._create_indexes()

    def _create_indexes(self):
        self.database["users"].create_index("username", unique=True)
        self.database["users"].create_index("email", unique=True)
        self.database["tasks"].create_index("user_id")
        
    def disconnect(self):
        if self.client:
            self.client.close()
            
    def get_collection(self, name: str) -> Collection:
        return self.database[name]
    
db = MongoDB()
