import re

def remove_hidden_links(text: str) -> str:
    # Remove markdown style links [text](url)
    text = re.sub(r'\[.*?\]\(https?://\S+\)', '', text)

    # Remove naked links (http, https, www, t.me, telegram.me, etc.)
    text = re.sub(r'(https?://\S+|www\.\S+|t\.me/\S+|telegram\.me/\S+)', '', text)

    # Remove @usernames
    text = re.sub(r'@\w+', '', text)

    # Clean multiple spaces/newlines
    text = ' '.join(text.split())
    return text
