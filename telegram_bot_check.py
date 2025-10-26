import os
import telegram
from dotenv import load_dotenv
from save_tools import send_photo  


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    TELEGRAM_CHAT_ID = os.environ["TG_CHAT_ID"]
    TELEGRAM_PHOTO_PATH = os.getenv("TG_PHOTO_PATH", "default.jpg")

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_photo(bot, TG_CHAT_ID, TG_PHOTO_PATH, success_message=f"Картинка {TG_PHOTO_PATH} отправлена в канал!")
    

if __name__ == "__main__":
    main()
