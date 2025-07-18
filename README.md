# CNL-Auto-Post-Bot

A simple Telegram bot that automatically forwards new messages from one channel to another. You can configure multiple independent channel pairs like:

- Channel1 → Channel2  
- Channel3 → Channel4

> ❌ You **cannot** do chained forwarding like Channel1 → Channel2 → Channel3.

---

## ✅ Features

- Forward posts automatically from one channel to another.
- Supports multiple source → destination mappings.
- Admin commands to manage mappings.
- Built using Pyrogram + MongoDB.
- Easily deployable (Render, Koyeb, VPS, etc).

---

## 🌐 Environment Variables

You need to set the following variables (e.g., in `.env` or Render/Koyeb config):

```env
API_ID=your_api_id
API_HASH=your_api_hash
SESSION=your_bot_token
ADMINS=your_telegram_id_or_username
DB_URL=your_mongodb_connection_uri
