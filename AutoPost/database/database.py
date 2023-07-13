from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://filesautobot:filesautobot870@cluster0.qcxdkpw.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["auto-post"]
        self.collection = self.db["auto-post-collection"]
        self.block_collection = self.db["blocked-text"]
    
    def save_chat_ids(self, user_id, from_chat_id, to_chat_id):
        try:
            existing_data = self.collection.find_one({'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id})
            if existing_data:
                print("Chat IDs already exist in the database.")
            else:
                data = {'user_id': user_id, 'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id}
                self.collection.insert_one(data)
                print("Chat IDs saved to the database.")
        except Exception as e:
            print("Error occurred while saving chat IDs to the database:", str(e))

    def delete_chat_ids(self, from_chat_id, to_chat_id):
        try:
            delete_result = self.collection.delete_one({'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id})
            if delete_result.deleted_count > 0:
                print("Chat IDs deleted from the database.")
            else:
                print("Chat IDs not found in the database.")
        except Exception as e:
            print("Error occurred while deleting chat IDs from the database:", str(e))

    def get_chat_ids(self, from_chat_id):
        try:
            channels = self.collection.find_one(
                {
                    'from_chat_id': from_chat_id
                }
            )
            if channels:
                from_chat_id = channels["from_chat_id"]
                to_chat_id = channels["to_chat_id"]
                return from_chat_id, to_chat_id
            return None
        except Exception as e:
            print("Error occurred while retrieving chat IDs from the database:", str(e))

    def get_channels_for_user(self, user_id):
        try:
            channels = self.collection.find({'user_id': user_id})
            return list(channels)
        except Exception as e:
            print("Error occurred while retrieving channels for user from the database:", str(e))
            return []

    def add_block_text(self, user_id, from_chat_id, text):
        try:
            existing_data = self.block_collection.find_one({'user_id': user_id})
            if existing_data:
                self.block_collection.update_one({'from_chat_id': from_chat_id}, {'$push': {'texts': text}})
            else:
                data = {'user_id': user_id, 'from_chat_id': from_chat_id, 'texts': [text]}
                self.block_collection.insert_one(data)
            print("Block text added to the database.")
        except Exception as e:
            print("Error occurred while adding block text to the database:", str(e))

    def get_texts(self, from_chat_id):
        try:
            data = self.block_collection.find_one({'from_chat_id': from_chat_id})
            if data:
                return data['texts']
            return []
        except Exception as e:
            print("Error occurred while retrieving block texts from the database:", str(e))
            return []

    def delete_text(self, user_id, from_chat_id, text):
        try:
            data = self.block_collection.find_one({'user_id': user_id})
            if data:  
                self.block_collection.update_one({'from_chat_id': from_chat_id}, {'$pull': {'texts': text}})
                print("Block text deleted from the database.")
        except Exception as e:
            print("Error occurred while deleting block text from the database:", str(e))

    def delete_all_texts(self, user_id, from_chat_id):
        try:
            data = self.block_collection.find_one({'user_id': user_id})
            if data:    
                self.block_collection.update_one({'from_chat_id': from_chat_id}, {'$set': {'texts': []}})
                print("All block texts deleted from the database.")
        except Exception as e:
            print("Error occurred while deleting all block texts from the database:", str(e))

    def clear_database(self):
        try:
            self.collection.delete_many({})
            self.block_collection.delete_many({})
            print("Database cleared successfully.")
        except Exception as e:
            print("Error occurred while clearing the database:", str(e))     

    def delete_connection(self, user_id, from_chat_id, to_chat_id):
        try:
            existing = self.collection.find({'user_id': user_id})
            if existing:
                self.collection.delete_one({'from_chat_id': from_chat_id, 'to_chat_id': to_chat_id})
                print("Connection deleted from the database.")
        except Exception as e:
            print("Error occurred while deleting the connection:", str(e))
        try:
            existing = self.collection.find({'user_id': user_id})
            if existing:
                self.block_collection.delete_one({'from_chat_id': from_chat_id})
                print("Block texts for the connection deleted from the database.")
        except Exception as e:
            print("Error occurred while deleting block texts for the connection:", str(e))
