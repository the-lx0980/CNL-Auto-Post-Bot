def remove_content(text):
    text = text.replace("@MaxPlayHD", "").replace("👉", "")
    text = text.replace("Join Us On Telegram", "").replace("Support us", "").replace("🙏", "").replace("❤️", "")
    return text
