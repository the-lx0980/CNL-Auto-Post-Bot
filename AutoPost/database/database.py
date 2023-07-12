# (c) @TheLx0980
# Year : 2023
# Month : Jun
# Language : Python 3

from pymongo import MongoClient

class Database:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add_forwarding(self, user_id, from_chat_id, to_chat_id):
        existing_entry = self.collection.find_one({"user_id": user_id})
        if existing_entry:
            return False
        data = {
            "user_id": user_id,
            "from_chat_id": from_chat_id,
            "to_chat_id": to_chat_id
        }
        self.collection.insert_one(data)
        return True

    def get_forwarding(self, user_id):
        entry = self.collection.find_one({"user_id": user_id})
        if entry:
            from_chat_id = entry["from_chat_id"]
            to_chat_id = entry["to_chat_id"]
            return (from_chat_id, to_chat_id)
        return None

    def remove_forwarding(self, user_id):
        result = self.collection.delete_one({"user_id": user_id})
        return result.deleted_count > 0

    def remove_forwarding(self, user_id, from_chat_id, to_chat_id):
        result = self.collection.delete_one({"user_id": user_id, "from_chat_id": from_chat_id, "to_chat_id": to_chat_id})
        return result.deleted_count > 0
