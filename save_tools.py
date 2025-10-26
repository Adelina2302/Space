import os
from pathlib import Path
import telegram
from telegram.error import TelegramError


def create_save_dir(save_folder: str) -> Path:
    save_dir = Path(save_folder or "images")
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def send_photo(bot: telegram.Bot, chat_id: str, photo_path: str, success_message: str = None) -> bool:
    try:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
        print(success_message or f"Фото {photo_path} отправлено успешно!")
        return True
    except (FileNotFoundError, PermissionError, OSError) as e:
        print(f"Ошибка при работе с файлом {photo_path}: {e}")
    except TelegramError as e:
        print(f"Ошибка при отправке фото {photo_path}: {e}")
    return False
