import argparse
import os
import sys
import requests
from image_downloader import download_image, get_file_extension


def create_save_folder(save_folder: str) -> str:
    os.makedirs(save_folder, exist_ok=True)
    return save_folder


def fetch_apod_data(api_key: str, count: int) -> list[dict]:
    api_url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count={count}"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    data_list = response.json()
    if not data_list:
        raise ValueError("Фотографий APOD нет")
    return data_list


def extract_image_urls(data_list: list[dict]) -> list[str]:
    urls = []
    for data in data_list:
        url = data.get("hdurl") or data.get("url")
        if url:
            urls.append(url)
    return urls


def save_apod_images(urls: list[str], save_folder: str):
    for i, url in enumerate(urls, start=1):
        ext = get_file_extension(url)
        save_path = os.path.join(save_folder, f"nasa_apod{i}{ext}")
        download_image(url, save_path)


def fetch_multiple_apod(api_key: str, count=5, save_folder="images"):
    save_dir = create_save_folder(save_folder)
    data_list = fetch_apod_data(api_key, count)
    urls = extract_image_urls(data_list)
    save_apod_images(urls, save_dir)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Скачать APOD-фотографии NASA")
    parser.add_argument("--api_key", required=True, help="Ваш NASA API ключ")
    parser.add_argument("--count", type=int, default=5, help="Количество фото")
    parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
    args = parser.parse_args(argv)

    try:
        fetch_multiple_apod(args.api_key, args.count, args.save_folder)
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка при запросе к NASA API: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(0)
    except OSError as e:
        print(f"Ошибка при сохранении файла: {e}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
