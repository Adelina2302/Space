import os
import requests
from urllib.parse import urlsplit, unquote
from datetime import datetime
from download_tools import download_image


def get_file_extension(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, ext = os.path.splitext(filename)
    return ext


def fetch_hubble():
    save_folder = r"C:\sputnik_lesson#2\images"
    hubble_url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
    ext = get_file_extension(hubble_url)
    save_path = os.path.join(save_folder, f"hubble{ext}")
    download_image(hubble_url, save_path)


def fetch_spacex_last_launch():
    save_folder = r"C:\sputnik_lesson#2\images"
    api_url = "https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a"
    response = requests.get(api_url)
    data = response.json()
    photos = data["links"]["flickr"]["original"]

    if not photos:
        print("Фотографий SpaceX нет.")
    else:
        for i, link in enumerate(photos, start=1):
            ext = get_file_extension(link)
            filename = f"spacex{i}{ext}"
            save_path = os.path.join(save_folder, filename)
            download_image(link, save_path)


def fetch_multiple_apod(api_key, count=30):
    save_folder = r"C:\sputnik_lesson#2\images"
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


def fetch_epic_latest(api_key):
    api_url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={api_key}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к NASA EPIC API: {e}")
        return

    try:
        data = response.json()
    except ValueError as e:
        print(f"Ошибка обработки JSON: {e}")
        return

    if not data:
        print("Фотографий EPIC нет")
    else:
        latest_photo = data[0]
        image_name = latest_photo["image"]
        date = latest_photo["date"]
        year, month, day = date.split()[0].split("-")
        epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
        print("Ссылка на последнюю фотографию Земли EPIC:")
        print(epic_url)
        return epic_url


def fetch_multiple_epic(api_key, count=10):
    save_folder = r"C:\sputnik_lesson#2\images"
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
        date_str = photo["date"]
        date = datetime.fromisoformat(date_str)
        year, month, day = date.year, f"{date.month:02}", f"{date.day:02}"

        img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
        save_path = os.path.join(save_folder, f"epic_{i:02}.png")
        try:
            download_image(img_url, save_path)
        except Exception as e:
            print(f"Ошибка при скачивании {img_url}: {e}")


if __name__ == "__main__":
    api_key = "5OKv9XCdUJNe4vgC8rzYZSXq4Vcm9TKOjmcbptI6"
    fetch_hubble()
    fetch_spacex_last_launch()
    fetch_multiple_apod(api_key, count=30)
    fetch_epic_latest(api_key)
    fetch_multiple_epic(api_key, count=10)
