import os
import telegram
from dotenv import load_dotenv
from telegram.error import TelegramError


def send_photo(bot: telegram.Bot, chat_id: str, photo_path: str) -> bool:
    try:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        print(f"Картинка {photo_path} отправлена в канал!")
        return True
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Ошибка при работе с файлом {photo_path}: {e}")
    except TelegramError as e:
        print(f"Ошибка при отправке фото {photo_path}: {e}")
    return False


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    TG_CHAT_ID = os.environ["TG_CHAT_ID"]
    TG_PHOTO_PATH = os.getenv("TG_PHOTO_PATH", "default.jpg")

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_photo(bot, TG_CHAT_ID, TG_PHOTO_PATH)


if __name__ == "__main__":
    main()
