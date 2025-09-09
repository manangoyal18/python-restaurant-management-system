import pymongo
from pymongo import MongoClient
from django.conf import settings
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


class MongoDBConnection:
    """
    MongoDB connection utility for the restaurant management system.
    Provides singleton pattern for database connections.
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self.connect()

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            mongodb_settings = settings.MONGODB_SETTINGS
            self._client = MongoClient(mongodb_settings['host'])
            self._db = self._client[mongodb_settings['db_name']]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @property
    def client(self):
        return self._client

    @property
    def db(self):
        return self._db

    def get_collection(self, collection_name):
        """Get a specific collection"""
        return self._db[collection_name]

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()


# Singleton instance
mongodb = MongoDBConnection()


class MongoBaseModel:
    """Base model for MongoDB documents"""
    
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.collection = mongodb.get_collection(collection_name)
    
    def create(self, data):
        """Create a new document"""
        try:
            # Add ObjectId if not present
            if '_id' not in data:
                data['_id'] = ObjectId()
            
            # Set the custom ID field based on the ObjectId
            id_field = f"{self.collection_name}_id"
            if id_field not in data:
                data[id_field] = str(data['_id'])
            
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating document in {self.collection_name}: {e}")
            raise
    
    def find_one(self, filter_dict):
        """Find a single document"""
        try:
            return self.collection.find_one(filter_dict)
        except Exception as e:
            logger.error(f"Error finding document in {self.collection_name}: {e}")
            raise
    
    def find_many(self, filter_dict=None, skip=0, limit=None, sort=None):
        """Find multiple documents"""
        try:
            if filter_dict is None:
                filter_dict = {}
            
            cursor = self.collection.find(filter_dict)
            
            if sort:
                cursor = cursor.sort(sort)
            if skip > 0:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            
            return list(cursor)
        except Exception as e:
            logger.error(f"Error finding documents in {self.collection_name}: {e}")
            raise
    
    def count(self, filter_dict=None):
        """Count documents"""
        try:
            if filter_dict is None:
                filter_dict = {}
            return self.collection.count_documents(filter_dict)
        except Exception as e:
            logger.error(f"Error counting documents in {self.collection_name}: {e}")
            raise
    
    def update_one(self, filter_dict, update_dict):
        """Update a single document"""
        try:
            result = self.collection.update_one(filter_dict, {"$set": update_dict})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document in {self.collection_name}: {e}")
            raise
    
    def delete_one(self, filter_dict):
        """Delete a single document"""
        try:
            result = self.collection.delete_one(filter_dict)
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting document in {self.collection_name}: {e}")
            raise


# Model instances for each collection
UserModel = MongoBaseModel('user')
MenuModel = MongoBaseModel('menu')
FoodModel = MongoBaseModel('food')
TableModel = MongoBaseModel('table')
OrderModel = MongoBaseModel('order')
OrderItemModel = MongoBaseModel('orderItem')
InvoiceModel = MongoBaseModel('invoice')