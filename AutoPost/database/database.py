# (c) @TheLx0980
# Year : 2023
# Month : Jun
# Language : Python 3

from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://<your-mongodb-connection-string>")
        self.db = self.client["auto-post"]
        self.replace_collection = self.db["replace-text"]
        self.id_collection = self.db["id-collection"]

    def add_channel(self, channel_id, caption):
        existing_channel = self.id_collection.find_one({"channel_id": channel_id})
        if existing_channel:
            raise ValueError("Your channel is already available in the database.")

        channel_data = {"channel_id": channel_id, "caption": caption}
        self.id_collection.insert_one(channel_data)

    def delete_channel(self, channel_id):
        self.id_collection.delete_one({"channel_id": channel_id})

    def get_caption(self, channel_id):
        channel_data = self.id_collection.find_one({"channel_id": channel_id})
        if channel_data:
            from_chat_id = channel_data["channel_id"]
            m_caption = channel_data["caption"]
            return m_caption, from_chat_id
        return None

  
    def save_replace_text(self, channel_id, old_text, new_text):
        forward_data = self.get_forward_data(channel_id)
        if forward_data:
            # Check if the entry already exists
            replace_texts = forward_data['replace_texts']
            if any(data['old_text'] == old_text and data['new_text'] == new_text for data in replace_texts):
                return  # Entry already exists, do not add duplicate
            forward_data['replace_texts'].append({'old_text': old_text, 'new_text': new_text})
            self.replace_collection.update_one({'channel_id': channel_id}, {'$set': {'replace_texts': forward_data['replace_texts']}})
        else:
            data = {
                'channel_id': channel_id,
                'replace_texts': [{'old_text': old_text, 'new_text': new_text}]
            }
            self.replace_collection.insert_one(data)

    def get_forward_data(self, channel_id):
        return self.replace_collection.find_one({'channel_id': channel_id})

    def delete_replace_text(self, channel_id, old_text, new_text):
        try:
            delete_result = self.replace_collection.update_one({'channel_id': channel_id},
                                                               {'$pull': {'replace_texts': {'old_text': old_text, 'new_text': new_text}}})
            if delete_result.modified_count > 0:
                print("Replace text entry deleted from the database.")
            else:
                print("No replace text entry found for the channel and text.")
        except Exception as e:
            print("Error occurred while deleting replace text entry from the database:", str(e))

    def delete_all_replace_text(self, channel_id):
        try:
            delete_result = self.replace_collection.delete_many({'channel_id': channel_id})
            if delete_result.deleted_count > 0:
                print("All replace text entries deleted from the database.")
            else:
                print("No replace text entries found for the channel.")
        except Exception as e:
            print("Error occurred while deleting replace text entries from the database:", str(e))


