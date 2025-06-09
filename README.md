# Telegram Weather Bot with Admin Panel🌥️🌆🌤️ 

### TELEGRAM HANDLE - [@myskynews247bot](https://t.me/myskynews247bot)
A Telegram bot built with Node.js that allows users to subscribe to daily weather updates. It also features a web-based admin panel to manage bot settings (API keys) and user accounts (block/delete users).

---

## Features

- Users can `/subscribe` and `/unsubscribe`  to daily weather updates via Telegram commands.
- get weather update `/weather <city>` in seconds
- Admin panel to:
  - `/block <userid>` user
  - `/unblock <userid>` user
  
- Uses PostgreSQL to store users and settings.
- Fetches weather data from OpenWeatherMap API.
- Scheduled daily weather notifications.

---

## Tech Stack

- Python 3
- PostgreSQL
- Telegram Bot API 
- OpenWeatherMap API for weather data
- Admin panel Fast API 

---


### Installation

1. Clone the repo

   ```bash
   python -m venv weatherenv
   weatherenv/Script/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
