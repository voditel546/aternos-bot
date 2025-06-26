import asyncio
from datetime import datetime
from threading import Thread

from flask import Flask
from mcstatus import JavaServer
from telegram import Bot

# 🔧 Налаштування
BOT_TOKEN = '7968761400:AAGlkkcNI7XiSIWJK7DP6l9Dpk94jAKEF70'
CHAT_ID = -1002424017400
ADDRESS = "Na4narkamana.aternos.me"
PORT = 41833  # ⚠️ Перевір на сайті Aternos, може змінюватися

# 🤖 Ініціалізація
bot = Bot(token=BOT_TOKEN)
server = JavaServer(ADDRESS, PORT)
was_online = None  # Стартове значення (ще не знаємо)

# 🌐 Flask веб-сервер для Render
app = Flask(__name__)
@app.route("/")
def index():
    return "Bot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# 🔍 Функція перевірки сервера
async def check_server():
    global was_online
    now = datetime.now().strftime("%H:%M")
    try:
        status = server.status()
        print(f"[{now}] Сервер онлайн ({status.players.online} гравців)")

        if was_online is False or was_online is None:
            await asyncio.to_thread(bot.send_message, chat_id=CHAT_ID,
                                    text=f"🟢 Час {now}\nСервер відкрився!")
        was_online = True

    except Exception as e:
        print(f"[{now}] Сервер офлайн або недоступний: {e}")
        if was_online is True or was_online is None:
            await asyncio.to_thread(bot.send_message, chat_id=CHAT_ID,
                                    text=f"🔴 Час {now}\nСервер закрився!")
        was_online = False

# 🔁 Головний цикл
async def main_loop():
    while True:
        await check_server()
        await asyncio.sleep(60)

# 🚀 Старт Flask + бота
if __name__ == "__main__":
    Thread(target=run_flask).start()
    asyncio.run(main_loop())
