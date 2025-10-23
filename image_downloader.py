import os
import requests
from urllib.parse import urlsplit, unquote

def download_image(url, save_path):
    folder = os.path.dirname(save_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
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
