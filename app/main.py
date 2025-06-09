from fastapi import FastAPI
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
from app import bot
from app import admin
from app import database
from dotenv import load_dotenv
import os
import requests

print("CWD:", os.getcwd())

load_dotenv()

app = FastAPI()
bot_app = None

async def daily_weather(bot_app):
    while True:
        await asyncio.sleep(6)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
        users = database.all_users()
        apikey = "3ae6527032cc4a0f623ec1810c878fde"
        hyd = f"https://api.openweathermap.org/data/2.5/weather?q=hyderabad&appid={apikey}"
        delhi = f"https://api.openweathermap.org/data/2.5/weather?q=hyderabad&appid={apikey}"
        bang = f"https://api.openweathermap.org/data/2.5/weather?q=hyderabad&appid={apikey}"
        hyd1 = requests.get(hyd).json()
        delhi1 = requests.get(delhi).json()
        bang1 = requests.get(bang).json()
        if delhi1.get("main") and hyd1.get("main") and bang1.get("main") :
            hyderabad = hyd1['main']['temp']
            bangalore = bang1['main']['temp']
            delhi = delhi1['main']['temp']
            for user in users:
                print(user)
                try:
                    await bot_app.bot.send_message(chat_id=user[0],text=f"""
                        Todays Weathe Updates ☀️⛅🌧️

City 🌆         Temperature(°C)🌥️ 
                                                   
Hyderabad           {round(abs(hyderabad-273.15),2)}°C
Delhi                     {round(abs(delhi-273.15),2)}°C
Bangalore            {round(abs(bangalore-273.15),2)}°C
                    """)
                except Exception as e:
                    print(f"Error sending weather Update {e}")
        


@app.on_event("startup")
async def startup():
    global bot_app
    database.init_db()

    bot_app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()
    bot_app.add_handler(CommandHandler("start", bot.start))
    bot_app.add_handler(CommandHandler("weather", bot.weather))
    bot_app.add_handler(CommandHandler("block", admin.block))
    bot_app.add_handler(CommandHandler("unblock", admin.unblock))
    bot_app.add_handler(CommandHandler('subscribe',bot.subscribe))
    bot_app.add_handler(CommandHandler('unsubscribe',bot.unsubscribe))
    await bot_app.initialize()
    await bot_app.start()
    asyncio.create_task(bot_app.updater.start_polling())
    asyncio.create_task(daily_weather(bot_app))



@app.on_event("shutdown")
async def shutdown():
    await bot_app.updater.stop()
    await bot_app.stop()
    await bot_app.shutdown()

@app.get("/")
async def root():
    return {"status": "Bot is running"}
