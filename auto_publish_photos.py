import os
import time
import random
import argparse
import telegram

def get_all_images(directory, extensions=('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def publish_photos(bot, chat_id, photo_files, interval):
    while True:
        if not photo_files:
            print("Нет фотографий для публикации. Проверю снова через", interval, "секунд.")
            time.sleep(interval)
            continue

        random.shuffle(photo_files)
        for photo_path in photo_files:
            try:
                if os.path.getsize(photo_path) > 20_000_000:
                    print(f"Файл {photo_path} слишком большой (>20MB), пропущен.")
                    continue

                with open(photo_path, 'rb') as photo:
                    bot.send_photo(chat_id=chat_id, photo=photo)
                print(f"Опубликовано: {photo_path}")

            except Exception as e:
                print(f"Ошибка публикации {photo_path}: {e}")

            time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="Автоматическая публикация фото в Telegram-канал")

    parser.add_argument("--token", required=True, help="Токен Telegram-бота")
    parser.add_argument("--chat_id", required=True, help="Chat ID или username канала (@my_channel)")
    parser.add_argument("--photos_dir", required=True, help="Папка с фотографиями")
    parser.add_argument("--interval", type=int, default=4 * 60 * 60,
                        help="Интервал публикации в секундах (по умолчанию 4 часа)")

    args = parser.parse_args()

    bot = telegram.Bot(token=args.token)

    while True:
        photo_files = get_all_images(args.photos_dir)
        publish_photos(bot, args.chat_id, photo_files, args.interval)

if __name__ == "__main__":
    main()
