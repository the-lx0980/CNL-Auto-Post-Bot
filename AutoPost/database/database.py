from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://filesautobot:filesautobot870@cluster0.qcxdkpw.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["auto-post"]
        self.id_collection = self.db["channel-id"]
        self.block_collection = self.db["blocked-text"]
    
    def save_chat_ids(self, user_id, channel_id):
        try:
            existing_data = self.id_collection.find_one({'user_id': user_id})
            if existing_data:
                print("Chat IDs already exist in the database.")
            else:
                data = {'user_id': user_id, 'channel_id': channel_id}
                self.id_collection.insert_one(data)
                print("Chat IDs saved to the database.")
        except Exception as e:
            print("Error occurred while saving chat IDs to the database:", str(e))

    def delete_chat_ids(self, user_id, channel_id):
        try:
            existing_data = self.id_collection.find_one({'user_id': user_id})
            if existing_data:
                delete_result = self.id_collection.delete_one({'user_id': user_id, 'channel_id': channel_id})
                if delete_result.deleted_count > 0:
                    print("Chat IDs deleted from the database.")
                else:
                    print("Chat IDs not found in the database.")
        except Exception as e:
            print("Error occurred while deleting chat IDs from the database:", str(e))

    def get_channel_id(self, channel_id):
        try:
            channels = self.collection.find_one({'channel_id': channel_id})           
            if channels:
                return channels["channel_id"]
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

    def add_block_text(self, user_id, channel_id, text):
        try:
            existing_data = self.block_collection.find_one({'user_id': user_id, 'channel_id': channel_id})
            if existing_data:
                existing_texts = existing_data.get('texts', [])
                if text in existing_texts:
                    print("Text already exists in the database.")
                else:
                    self.block_collection.update_one({'user_id': user_id, 'channel_id': channel_id}, {'$push': {'texts': text}})
                    print("Block text added to the database.")
            else:
                data = {'user_id': user_id, 'channel_id': channel_id, 'texts': [text]}
                self.block_collection.insert_one(data)
                print("Block text added to the database.")
        except Exception as e:
            print("Error occurred while adding block text to the database:", str(e))

    def get_block_texts(self, channel_id):
        try:
            data = self.block_collection.find_one({'channel_id': channel_id})
            if data:
                return data['texts']
            return []
        except Exception as e:
            print("Error occurred while retrieving block texts from the database:", str(e))
            return []

    def delete_block_text(self, channel_id, text):
        try:
            data = self.block_collection.find_one({'channel_id': channel_id})
            if data:  
                self.block_collection.update_one({'channel_id': channel_id}, {'$pull': {'texts': text}})
                print("Block text deleted from the database.")
        except Exception as e:
            print("Error occurred while deleting block text from the database:", str(e))

    def delete_all_block_texts(self, user_id, channel_id):
        try:
            data = self.block_collection.find_one({'user_id': user_id})
            if data:    
                self.block_collection.update_one({'channel_id': channel_id}, {'$set': {'texts': []}})
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
