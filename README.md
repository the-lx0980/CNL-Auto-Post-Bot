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
       (Use spaces to separate multiple admin IDs or usernames.)
DB_URL=your_mongodb_connection_uri
```
---
## 📚 Bot Commands

> Below are examples along with each command to help you set up quickly.

### 🔘 Channel Mappings

* **/add\_channel** - Add a channel to the database with a caption.
  **Format:** `/add_channel (from_chat) (to_chat) (end_text)`
  **Example:**

  ```bash
  /add_channel -1001234567890 -1009876543210 !()!
  ```

* **/delete\_channel** - Delete a channel from the database.
  **Format:** `/delete_channel (channel_id)`
  **Example:**

  ```bash
  /delete_channel -1001234567890
  ```

### ✏️ Text Replacing

* **/add\_replace\_text** - Add replace text rule.
  **Format:** `/add_replace_text (channel_id) |:| (old_text) |:| (new_text)`
  **Example:**

  ```bash
  /add_replace_text -1001234567890 |:| Hello |:| Hi
  ```

* **/delete\_replace\_text** - Remove one replace rule.
  **Format:** `/delete_replace_text (channel_id) (old_text)`
  **Example:**

  ```bash
  /delete_replace_text -1001234567890 Hello
  ```

* **/del\_all\_replace** - Remove all replace texts (admins only).
  **Format:** `/del_all_replace (channel_id)`
  **Example:**

  ```bash
  /del_all_replace -1001234567890
  ```

### 🚫 Text Blocking

* **/save\_blocked\_text** - Add blocked word.
  **Format:** `/save_blocked_text (channel_id) (block_text)`
  **Example:**

  ```bash
  /save_blocked_text -1001234567890 spam
  ```

* **/get\_blocklist** - List all blocked words.
  **Format:** `/get_blocklist (channel_id)`
  **Example:**

  ```bash
  /get_blocklist -1001234567890
  ```

* **/del\_block\_text** - Remove one blocked word.
  **Format:** `/del_block_text (channel_id) (block_text)`
  **Example:**

  ```bash
  /del_block_text -1001234567890 spam
  ```

* **/del\_blocklist** - Remove all blocked words.
  **Format:** `/del_blocklist (channel_id)`
  **Example:**

  ```bash
  /del_blocklist -1001234567890
  ```

### 📂 Admin Utility

* **/cleardb** - Delete all info from the database
  *(Admins only)*
  **Example:**

  ```bash
  /cleardb
  ```

---

## 🔧 Example

```bash
/add_channel -1001234567890 -1009876543210 !()!
```

This will forward posts from Channel A to Channel B with no extra caption.

---
