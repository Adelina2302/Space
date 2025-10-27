import os
import random
import telegram
from dotenv import load_dotenv
from save_tools import send_photo


def main():
    load_dotenv()
    TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
    TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
    IMAGES_FOLDER = os.getenv("TELEGRAM_IMAGES_FOLDER", "images")

    
    if not os.path.isdir(IMAGES_FOLDER):
        print(f"Папка {IMAGES_FOLDER} не найдена.")
        return

    image_files = [
        f for f in os.listdir(IMAGES_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print(f"В папке {IMAGES_FOLDER} нет изображений.")
        return

    
    random_image = random.choice(image_files)
    image_path = os.path.join(IMAGES_FOLDER, random_image)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_photo(
        bot,
        TELEGRAM_CHAT_ID,
        image_path,
        success_message=f"Отправлено случайное фото: {random_image}"
    )


if __name__ == "__main__":
    main()
