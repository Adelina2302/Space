import argparse
import os
import requests
from image_downloader import download_image, get_file_extension

def fetch_multiple_apod(api_key, count=5, save_folder="images"):
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count={count}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к NASA API: {e}")
        return

    try:
        data_list = response.json()
    except ValueError as e:
        print(f"Ошибка обработки JSON: {e}")
        return

    for i, data in enumerate(data_list, start=1):
        url = data.get("hdurl") or data.get("url")
        if not url:
            print(f"Картинка {i} отсутствует")
            continue
        ext = get_file_extension(url)
        save_path = os.path.join(save_folder, f"nasa_apod{i}{ext}")
        try:
            download_image(url, save_path)
        except Exception as e:
            print(f"Ошибка при скачивании или сохранении картинки {i}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачать APOD-фотографии NASA")
    parser.add_argument("--api_key", required=True, help="Ваш NASA API ключ")
    parser.add_argument("--count", type=int, default=5, help="Количество фото")
    parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
    args = parser.parse_args()
    fetch_multiple_apod(args.api_key, args.count, args.save_folder)