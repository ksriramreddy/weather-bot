from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from app import database
import requests

async def start(update : Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"""
        🌤️ Hello {user.first_name}!

Welcome to the Weather Bot ☀️⛅🌧️

Here's what you can do:
📍 Use /weather <city> – to get current weather for any city
🔔 Use /subscribe – to get daily automatic weather updates
🚫 Use /unsubscribe – to stop receiving daily updates

Example: `/weather Hyderabad`

Stay updated, rain or shine! 🌦️🌈

""" 
    )
    return

async def weather(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_user.id,action=ChatAction.TYPING)
    if not context.args:
        await update.message.reply_text(
            """ use "/weather <city>" properly """
        ) 
        return
    city = " ".join(context.args)
    apikey = "3ae6527032cc4a0f623ec1810c878fde"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}"
    resp = requests.get(url).json()
    if resp.get("main"):
        weather_desc = resp['weather'][0]['description']
        temp = resp['main']['temp']
        await update.message.reply_text(f"{city}: {round(abs(temp-273.15),2)}°C, {weather_desc}")
    else:
        await update.message.reply_text("City not found.")

async def subscribe(update : Update, context : ContextTypes):
    telegram_id,username = update.effective_user.id,update.effective_user.first_name
    database.add_subscription(telegram_id,username)
    await update.message.reply_text("✅ Subscribed to daily weather updates!")

async def unsubscribe(update : Update, context : ContextTypes):
    telegram_id = update.effective_user.id
    print(type(telegram_id))
    database.remove_subscription(telegram_id)
    await update.message.reply_text("❌ Unsubscribed from daily updates.")
    
