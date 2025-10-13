import os
import telegram
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_CHAT_ID = os.getenv("CHAT_ID")
PHOTO_PATH = os.getenv("PHOTO_PATH")


if not TOKEN or not CHANNEL_CHAT_ID or not PHOTO_PATH:
    raise ValueError("Не заданы переменные окружения")

bot = telegram.Bot(token=TOKEN)
with open(PHOTO_PATH, 'rb') as photo:
    bot.send_photo(chat_id=CHANNEL_CHAT_ID, photo=photo)

print('Картинка отправлена в канал!')
