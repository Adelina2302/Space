import requests
import argparse
from pathlib import Path
from image_downloader import download_image, get_file_extension


def create_save_dir(save_folder: str) -> Path:
    save_dir = Path(save_folder or "images")
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def fetch_spacex_data(api_url: str) -> dict:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_photo_links(data: dict) -> list[str]:
    if not data:
        return []
    return data.get("links", {}).get("flickr", {}).get("original", []) or []


def save_spacex_photos(photo_links: list[str], save_dir: Path):
    if not photo_links:
        print("Фотографий SpaceX нет.")
        return

    for i, link in enumerate(photo_links, start=1):
        sanitized_link = link.replace("\\", "/")
        ext = get_file_extension(sanitized_link)
        save_path = save_dir / f"spacex{i}{ext}"
        download_image(sanitized_link, str(save_path))

    print(f"Скачано {len(photo_links)} фото в {save_dir}")


def fetch_spacex_images(api_url: str, save_folder: str):
    save_dir = create_save_dir(save_folder)
    data = fetch_spacex_data(api_url)
    photo_links = extract_photo_links(data)
    save_spacex_photos(photo_links, save_dir)


def main():
    parser = argparse.ArgumentParser(description="Скачать фотографии последнего запуска SpaceX")
    parser.add_argument("--api_url", required=True, help="URL API SpaceX для конкретного запуска")
    parser.add_argument("--save_folder", default="images", help="Папка для сохранения фото")
    args = parser.parse_args()

    try:
        fetch_spacex_images(args.api_url, args.save_folder)
    except requests.RequestException as exc:
        print(f"Ошибка при запросе API: {exc}")
    except Exception as exc:
        print(f"Произошла непредвиденная ошибка: {exc}")


if __name__ == "__main__":
    main()
