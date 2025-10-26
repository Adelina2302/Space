import os
import time
import random
import argparse
import telegram
from telegram.error import TelegramError
from typing import List, Tuple
from save_tools import send_photo 

MAX_FILE_SIZE = 20_000_000
MAX_FILE_SIZE_MB = MAX_FILE_SIZE / 1_000_000
DEFAULT_PUBLISH_INTERVAL_HOURS = 4
SECONDS_IN_HOUR = 60 * 60
DEFAULT_PUBLISH_INTERVAL = DEFAULT_PUBLISH_INTERVAL_HOURS * SECONDS_IN_HOUR


def get_all_images(directory: str, extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')) -> List[str]:
    file_list: List[str] = []
    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                file_list.append(os.path.join(root, file))
    return file_list


def filter_valid_photos(photo_files: List[str]) -> List[str]:
    valid_photos = []
    for photo_path in photo_files:
        try:
            size = os.path.getsize(photo_path)
            if size <= MAX_FILE_SIZE:
                valid_photos.append(photo_path)
            else:
                print(f"Файл {photo_path} слишком большой (>{MAX_FILE_SIZE_MB:.0f}MB), пропущен.")
        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"Ошибка с файлом {photo_path}: {e}")
    return valid_photos


def publish_photo_batch(bot: telegram.Bot, chat_id: str, photo_files: List[str], interval: int):
    random.shuffle(photo_files)
    valid_photos = filter_valid_photos(photo_files)
    for photo_path in valid_photos:
        send_photo(bot, chat_id, photo_path, success_message=f"Опубликовано: {photo_path}")
        time.sleep(interval)


def publish_photos(bot: telegram.Bot, chat_id: str, photos_dir: str, interval: int):
    while True:
        photo_files = get_all_images(photos_dir)
        if not photo_files:
            print(f"Нет фотографий для публикации. Проверю снова через {interval} секунд.")
            time.sleep(interval)
            continue
        publish_photo_batch(bot, chat_id, photo_files, interval)


def main():
    parser = argparse.ArgumentParser(description="Автоматическая публикация фото в Telegram-канал")
    parser.add_argument("--token", required=True, help="Токен Telegram-бота")
    parser.add_argument("--chat_id", required=True, help="Chat ID или username канала (@my_channel)")
    parser.add_argument("--photos_dir", required=True, help="Папка с фотографиями")
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_PUBLISH_INTERVAL,
        help=f"Интервал публикации в секундах (по умолчанию {DEFAULT_PUBLISH_INTERVAL_HOURS} часа)"
    )
    args = parser.parse_args()

    bot = telegram.Bot(token=args.token)

    try:
        publish_photos(bot, args.chat_id, args.photos_dir, args.interval)
    except KeyboardInterrupt:
        print("Прервано пользователем")
    except TelegramError as e:
        print(f"Ошибка Telegram API: {e}")
    except OSError as e:
        print(f"Ошибка файловой системы: {e}")


if __name__ == "__main__":
    main()
