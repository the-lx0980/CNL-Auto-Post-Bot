# (c) @TheLx0980
# Year: 2023
# Month: Jun
# Language: Python 3

from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://filesautobot:filesautobot870@cluster0.qcxdkpw.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["auto-post"]
        self.replace_collection = self.db["replace-text"]
        self.id_collection = self.db["id-collection"]

    def add_channel(self, channel_id, to_chat, caption):
        existing_channel = self.id_collection.find_one({"channel_id": channel_id})
        if existing_channel:
            raise ValueError("Your channel is already available in the database.")

        channel_data = {"channel_id": channel_id, "to_chat": to_chat, "caption": caption}
        self.id_collection.insert_one(channel_data)

    def delete_channel(self, channel_id):
        chat = self.id_collection.find_one({'channel_id': channel_id})
        if chat:
            self.id_collection.delete_many({"channel_id": channel_id})
            return channel_id
        return None

    def get_caption(self, channel_id):
        channel_data = self.id_collection.find_one({"channel_id": channel_id})
        if channel_data:
            from_chat = channel_data["channel_id"]
            to_chat = channel_data["to_chat"]
            m_caption = channel_data["caption"]
            if not m_caption:
                m_caption = None
            return from_chat, to_chat, m_caption
        return None

    def save_replace_text(self, channel_id, old_text, new_text):
        replace_texts = self.get_replace_data(channel_id)
        if replace_texts:
            if any(data['old_text'] == old_text and data['new_text'] == new_text for data in replace_texts):
                print("Replace text entry already exists.")
                return

            replace_texts.append({'old_text': old_text, 'new_text': new_text})
            self.replace_collection.update_one({'channel_id': channel_id}, {'$set': {'replace_texts': replace_texts}})
            print("Replace text added successfully.")
        else:
            data = {
                'channel_id': channel_id,
                'replace_texts': [{'old_text': old_text, 'new_text': new_text}]
            }
            self.replace_collection.insert_one(data)
            print("Replace text added successfully.")

    def get_replace_data(self, channel_id):
        replace_data = self.replace_collection.find_one({'channel_id': channel_id})
        if replace_data:
            return replace_data['replace_texts']
        return None

    def delete_replace_text(self, channel_id, old_text, new_text):
        deleted_text = self.replace_collection.update_one({'channel_id': channel_id},
                                                          {'$pull': {'replace_texts': {'old_text': old_text, 'new_text': new_text}}})
        if deleted_text.modified_count > 0:
            print("Replace text deleted successfully.")
        else:
            print("No replace text found for the given channel ID and text.")

    def delete_all_replace_text(self, channel_id):
        deleted_texts = self.replace_collection.delete_many({'channel_id': channel_id})
        if deleted_texts.deleted_count > 0:
            return deleted_texts.deleted_count
            print("All replace texts deleted successfully.")
        else:
            print("No replace texts found for the given channel ID.")
