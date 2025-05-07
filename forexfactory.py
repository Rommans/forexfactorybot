from dotenv import load_dotenv
load_dotenv()

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from pytz import timezone
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler


API_TOKEN = os.getenv("API_TOKEN")
YOUR_CHAT_ID = int(os.getenv("YOUR_CHAT_ID"))

bratislava_tz = timezone("Europe/Bratislava")
TARGET_CURRENCIES = {"EUR", "GBP", "USD"}

def get_forex_news():
    # parsing
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.xml"
    response = requests.get(url)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    
    # for testing
    # with open("ff_calendar_thisweek.xml", "rb") as f:
    #     root = ET.fromstring(f.read())

    news_this_week = []
    news_today = []

    today_str = datetime.now(bratislava_tz).strftime("%b %d, %Y")
    today = datetime.strptime(today_str, "%b %d, %Y").date()

    for event in root.findall("event"):
        country = event.find("country").text.strip()
        impact = event.find("impact").text.strip()
        if impact != "High" or country not in TARGET_CURRENCIES:
            continue

        title = event.find("title").text.strip()
        date = event.find("date").text.strip()
        time = event.find("time").text.strip()

        forecast_element = event.find("forecast")
        forecast = forecast_element.text.strip() if forecast_element is not None and forecast_element.text else "N/A"

        previous_element = event.find("previous")
        previous = previous_element.text.strip() if previous_element is not None and previous_element.text else "N/A"

        # link = event.find("url").text.strip()

        try:
            event_date = datetime.strptime(date, "%m-%d-%Y").date()
        except ValueError:
            continue

        msg = (
            f"🔴 {date} {time} | {country}\n"
            f"🟢 <b>{title}</b>\n"
            f"📈 Forecast: {forecast}, Previous: {previous}"
        )

        news_this_week.append(msg)

        if event_date == today:
            news_today.append(msg)

    return news_this_week, news_today

def format_news_for_telegram(week_news, today_news):
    message = "🗓️ <b>Тиждень:</b>\n"
    message += "\n\n".join(week_news) if week_news else "Немає важливих подій цього тижня."
    message += "\n\n\n📆 <b>Сьогодні:</b>\n"
    message += "\n\n".join(today_news) if today_news else "Немає важливих подій сьогодні."
    return message

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привіт! Надішли /news, щоб отримати важливі події з ForexFactory.")

def send_news(update: Update, context: CallbackContext):
    week, today = get_forex_news()
    msg = format_news_for_telegram(week, today)
    update.message.reply_text(msg, parse_mode="HTML")

def auto_send_news():
    bot = Bot(token=API_TOKEN)
    week, today = get_forex_news()
    msg = format_news_for_telegram(week, today)
    bot.send_message(chat_id=YOUR_CHAT_ID, text=msg, parse_mode="HTML")

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("news", send_news))

    scheduler = BackgroundScheduler()
    scheduler.add_job(auto_send_news, trigger="cron", hour=8, minute=0, timezone=bratislava_tz)
    scheduler.start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()