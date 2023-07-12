# (c) @TheLx0980
# Year : 2023
# Month : Jun
# Language : Python 3

from pymongo import MongoClient

class Database:
    def __init__(self):
        connection_string = "mongodb+srv://filesautobot:filesautobot870@cluster0.qcxdkpw.mongodb.net/?retryWrites=true&w=majority"
        database_name = "auto post"
        collection_name = "auto-post-collection"

        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def add_forwarding(self, from_chat_id, to_chat_id):
        # Check if the entry already exists
        existing_entry = self.collection.find_one({"from_chat_id": from_chat_id, "to_chat_id": to_chat_id})
        if existing_entry:
            return False

        data = {
            "from_chat_id": from_chat_id,
            "to_chat_id": to_chat_id
        }
        self.collection.insert_one(data)
        return True

    def get_forwarding(self):
        # Retrieve all entries from the database
        entries = self.collection.find({})
        forwarding = []
        for entry in entries:
            forwarding.append((entry["from_chat_id"], entry["to_chat_id"]))
        return forwarding

