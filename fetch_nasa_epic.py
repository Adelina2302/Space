import argparse
import os
import requests
from image_downloader import download_image, get_file_extension
from datetime import datetime

parser = argparse.ArgumentParser(description="Скачать фото EPIC NASA")
parser.add_argument("--api_key", required=True, help="Ваш NASA API ключ")
parser.add_argument("--count", type=int, default=5, help="Количество фото")
parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
args = parser.parse_args()

def fetch_multiple_epic(api_key, count=5, save_folder="images"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    api_url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={api_key}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Ошибка запроса к NASA EPIC API: {e}")
        return

    if not data:
        print("Фотографий EPIC нет")
        return

    for i, photo in enumerate(data[:count], start=1):
        image_name = photo["image"]
        date_str = photo["date"]  # формат: "YYYY-MM-DD HH:MM:SS"
        date = datetime.fromisoformat(date_str)
        year, month, day = date.year, f"{date.month:02}", f"{date.day:02}"

        img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
        save_path = os.path.join(save_folder, f"epic_{i:02}.png")
        try:
            download_image(img_url, save_path)
        except Exception as e:
            print(f"Ошибка при скачивании {img_url}: {e}")

if __name__ == "__main__":
    fetch_multiple_epic(args.api_key, args.count, args.save_folder)
