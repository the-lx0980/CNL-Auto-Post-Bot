# CNL-Auto-Post-Bot

A simple Telegram bot that automatically forwards new messages from one channel to another. You can configure multiple independent channel pairs like:

- Channel1 → Channel2  
- Channel3 → Channel4

> ❌ You **cannot** do chained forwarding like Channel1 → Channel2 → Channel3.

---

## ✅ Features

* 📤 **Auto Forwarding**: Automatically forward posts from one Telegram channel to another.
* 🔁 **One-to-One Channel Mapping**: Create multiple individual source → destination mappings.
* ✏️ **Text Replacing**: Automatically replace defined words/phrases in forwarded messages.
* 🚫 **Text Blocking**: Prevent certain words or phrases from being forwarded.
* 📋 **Admin Commands**: Easy-to-use admin commands for setting up channels and rules.
* 🧠 **Caption Customization**: Add an end text or caption to forwarded messages.
* 💾 **MongoDB Database**: Efficient storage for all channel configurations and rules.
* ⚙️ **Deploy Anywhere**: Works on Render, Koyeb, Railway, Heroku, or your own VPS.

---

## 🌐 Environment Variables

You need to set the following variables (e.g., in `.env` or Render/Koyeb config):

```env
API_ID=your_api_id
API_HASH=your_api_hash
SESSION=your_bot_token
ADMINS=your_telegram_id_or_username
DB_URL=your_mongodb_connection_uri
```
