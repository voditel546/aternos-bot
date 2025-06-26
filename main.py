from mcstatus import JavaServer
from telegram import Bot
import asyncio
from datetime import datetime
from threading import Thread
from flask import Flask

BOT_TOKEN = '7968761400:AAGlkkcNI7XiSIWJK7DP6l9Dpk94jAKEF70'
CHAT_ID = -1002424017400
ADDRESS = "Na4narkamana.aternos.me"
PORT = 41833

bot = Bot(token=BOT_TOKEN)
server = JavaServer(ADDRESS, PORT)
was_online = False

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

async def check_server():
    global was_online
    now = datetime.now().strftime("%H:%M")
    try:
        status = server.status()
        if not was_online:
            await bot.send_message(chat_id=CHAT_ID, text=f"🟢 Час {now}\nСервер відкрився!")
            was_online = True
    except:
        if was_online:
            await bot.send_message(chat_id=CHAT_ID, text=f"🔴 Час {now}\nСервер закрився!")
            was_online = False

async def main_loop():
    while True:
        await check_server()
        await asyncio.sleep(60)

def run_flask():
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # Запускаємо Flask у окремому потоці
    Thread(target=run_flask).start()
    # Запускаємо головний цикл бота
    asyncio.run(main_loop())
