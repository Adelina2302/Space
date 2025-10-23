import argparse
import os
import sys
import requests
from requests.exceptions import RequestException
from json import JSONDecodeError
from image_downloader import download_image
from datetime import datetime
from urllib.parse import quote


def create_session():
    return requests.Session()


def fetch_epic_metadata(api_key, session):
    base_api_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}
    response = session.get(base_api_url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def build_epic_image_url(image_name, date_str, api_key):
    date = datetime.fromisoformat(date_str)
    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    quoted_image = quote(image_name, safe="")
    return f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{quoted_image}.png?api_key={api_key}"


def prepare_save_path(save_folder, index):
    return os.path.join(save_folder, f"epic_{index:02}.png")


def get_epic_image_urls(api_key, count, session):
    data = fetch_epic_metadata(api_key, session)
    if not data:
        raise ValueError("Фотографий EPIC нет")
    urls = []
    for photo in data[:count]:
        image_name = photo["image"]
        date_str = photo["date"]
        urls.append(build_epic_image_url(image_name, date_str, api_key))
    return urls


def download_epic_images(urls, save_folder):
    os.makedirs(save_folder, exist_ok=True)
    for i, url in enumerate(urls, start=1):
        save_path = prepare_save_path(save_folder, i)
        download_image(url, save_path)


def fetch_multiple_epic(api_key, count=5, save_folder="images"):
    session = create_session()
    urls = get_epic_image_urls(api_key, count, session)
    download_epic_images(urls, save_folder)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Скачать фото EPIC NASA")
    parser.add_argument("--api_key", required=True, help="Ваш NASA API ключ")
    parser.add_argument("--count", type=int, default=5, help="Количество фото")
    parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
    args = parser.parse_args(argv)

    try:
        fetch_multiple_epic(args.api_key, args.count, args.save_folder)
    except RequestException as e:
        print(f"Сетевая ошибка при запросе к NASA EPIC API: {e}", file=sys.stderr)
        sys.exit(2)
    except JSONDecodeError as e:
        print(f"Не удалось разобрать ответ API как JSON: {e}", file=sys.stderr)
        sys.exit(4)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(0)
    except OSError as e:
        print(f"Ошибка при доступе к файловой системе: {e}", file=sys.stderr)
        sys.exit(3)
    except KeyboardInterrupt:
        print("Прервано пользователем", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
