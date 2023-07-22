# (c) @TheLx0980
# Year : 2023
# Time : 14:40
# Month : July
# Date : 22


from AutoPost.database import Database 

db = Database()  

def contains_blocked_text(media_caption, channel_id):
    blocked_texts = db.get_all_blocked_texts(channel_id)
    if blocked_texts:
        for blocked_text in blocked_texts:
            if blocked_text in media_caption:
                return True
    return False
