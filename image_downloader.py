import os
import requests
from urllib.parse import urlsplit, unquote


def download_image(url, save_path):
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")

    if not isinstance(save_path, str) or not save_path.strip():
        raise ValueError("Save path must be a non-empty string.")

    folder = os.path.dirname(save_path)
    if folder and not os.path.exists(folder):
        raise FileNotFoundError(f"Directory does not exist: {folder}")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(save_path, "wb") as file:
        file.write(response.content)

    print(f"Картинка сохранена: {save_path}")


def get_file_extension(url):
    path = urlsplit(url).path
    filename = os.path.basename(unquote(path))
    _, ext = os.path.splitext(filename)
    return ext
