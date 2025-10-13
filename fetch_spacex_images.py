import requests
import argparse
from image_downloader import download_image, get_file_extension

# argparse
parser = argparse.ArgumentParser(description="Скачать фотографии последнего запуска SpaceX")
parser.add_argument("--api_url", required=True, help="URL API SpaceX для конкретного запуска")
parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
args = parser.parse_args()

def fetch_spacex_images(api_url, save_folder):
    
    if not save_folder:
        save_folder = "images"

    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    photos = data["links"]["flickr"]["original"]

    if not photos:
        print("Фотографий SpaceX нет.")
    else:
        for i, link in enumerate(photos, start=1):
            ext = get_file_extension(link)
            
            save_path = f"{save_folder}/spacex{i}{ext}"
            download_image(link, save_path)
        print(f"Скачано {len(photos)} фото.")

if __name__ == "__main__":
    fetch_spacex_images(args.api_url, args.save_folder)
