from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client: MongoClient = None
        self.database: Database = None
        
    def connect(self):
        self.client = MongoClient(settings.mongo_uri)
        self.database = self.client[settings.database_name]
        
    def disconnect(self):
        if self.client:
            self.client.close()
            
    def get_collection(self, name: str) -> Collection:
        return self.database[name]
    
db = MongoDB()
        