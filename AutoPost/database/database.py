# (c) @TheLx0980
# Year : 2023
# Month : Jun
# Language : Python 3

from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://filesautobot:filesautobot870@cluster0.qcxdkpw.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["auto-post"]
        self.collection = self.db["auto-post-collection"]
  
    def save_chat_ids(self, from_chat_id, to_chat_id):
        existing_data = self.collection.find_one({'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id})
        if existing_data:
            print("Chat IDs already exist in the database.")
        else:
            data = {'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id}
            self.collection.insert_one(data)
            print("Chat IDs saved to the database.")

    def delete_chat_ids(self, from_chat_id, to_chat_id):
        delete_result = self.collection.delete_one({'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id})
        if delete_result.deleted_count > 0:
            print("Chat IDs deleted from the database.")
        else:
            print("Chat IDs not found in the database.")

    def get_chat_ids(self, from_chat_id):
        return self.collection.find_one(
            {
                'to_chat_id': to_chat_id
            }
        )
