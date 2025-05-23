# 📈 ForexFactory High-Impact News Telegram Bot

This bot sends high-impact economic events from ForexFactory directly to your Telegram, including today's and this week's events. It works both via the `/news` command and automatically every day at 8:00 AM Bratislava time.

---

## 🚀 Quick Start

### 1. Clone the repository
```
git clone https://github.com/your-username/forexfactory-bot.git
cd forexfactory-bot
```

### 2. Create a .env file
```
API_TOKEN=your_telegram_bot_token_from_BotFather
YOUR_CHAT_ID=your_chat_id_for_sending_news
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the bot locally
```
python forexfactory.py
```

### 🧩 Bot Commands
```
/start — greeting message

/news — send the list of important events for the week and today
```

### 📦 Project Structure
```
.
├── forexfactory.py         # main bot code
├── requirements.txt        # list of dependencies
├── .env.example            # example of environment variables
├── Procfile                # deployment instructions (Railway)
└── README.md               # this file
```

### 📅 Automatic News Sending
The bot will send daily news at 8:00 AM Bratislava time, using APScheduler.