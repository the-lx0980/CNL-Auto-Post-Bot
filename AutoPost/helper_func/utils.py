# (c) @TheLx0980
# Year : 2023
# Time : 14:40
# Month : July
# Date : 22

import re
from AutoPost.database import Database 

db = Database()  

def contains_blocked_text(media_caption, channel_id):
    blocked_texts = db.get_all_blocked_texts(channel_id)
    if blocked_texts:
        for blocked_text in blocked_texts:
            if blocked_text in media_caption:
                return True
    return False

def remove_hidden_links(text: str) -> str:
    text = re.sub(r'\[.*?\]\(https?://\S+\)', '', text)
    text = re.sub(r'(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+)', '', text)
    text = re.sub(r'@\w+', '', text)
    text = ' '.join(text.split())
    return text
