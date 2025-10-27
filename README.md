# Проект: Автопубликация и скачивание фото из NASA и SpaceX

Данный репозиторий содержит: 
- Набор скриптов для скачивания космических фотографий (NASA APOD, NASA EPIC, SpaceX, Hubble) и автоматической публикации изображений в Telegram-канал с помощью бота.
- Скрипты находятся в корне репозитория:
  - auto_publish_photos.py — автоматическая публикация фото в Telegram-канал
  - fetch_nasa_apod.py — скачивание APOD (Photo of the Day) от NASA
  - fetch_nasa_epic.py — скачивание EPIC (Earth Polychromatic Imaging Camera) от NASA
  - fetch_spacex_images.py — скачивание фото из ответа API SpaceX (для конкретного запуска)
  - telegram_bot_check.py — утилита для проверки отправки одной фотографии через бота
  - image_downloader.py — функции для скачивания изображений (используются в других скриптах)
  - requirements.txt — список зависимостей проекта  
- Минимальные требования: Python 3.8+

Содержание
1. Требования и установка
2. Подготовка окружения 
3. Переменные окружения и .env
4. Описание и примеры запуска для каждого скрипта
5. Проверка результата и типичные ошибки


1) Требования и установка
- Рекомендуется создавать виртуальное окружение.
- Клонируем репозиторий и устанавливаем зависимости:

```bash
git clone https://github.com/Adelina2302/Space.git
cd Space
python -m venv .venv
# на Windows
.venv\Scripts\activate
# на macOS / Linux
source .venv/bin/activate

# установить зависимости (создайте файл requirements.txt)
pip install -r requirements.txt
```

Рекомендуемый requirements.txt (в корне проекта):
- requests
- python-telegram-bot 
- python-dotenv


2) Подготовка окружения (виртуальное окружение)
- Откройте новую консоль перед тестированием.
- Создайте и активируйте виртуальное окружение.
- Установите зависимости в виртуальном окружении.

3) Переменные окружения и .env
Некоторые скрипты используют переменные окружения (через python-dotenv в telegram_bot_check.py). Для удобства создайте файл `.env` в корне проекта с содержимым (пример):

```env
# .env - пример
TELEGRAM_TOKEN=<Ваш Telegram бот токен>
TELEGRAM_CHAT_ID=@my_channel_or_chat_id
TELEGRAM_PHOTO_PATH=images/sample.jpg
```

Примечание:
- auto_publish_photos.py в текущей реализации не читает .env — он принимает параметры через CLI: --token, --chat_id, --photos_dir, --interval. Для тестов используйте telegram_bot_check.py (он читает .env).
- Обязательно храните реальные токены и ключи в .env и не коммитьте их в публичный репозиторий.

4) Описание скриптов и примеры запуска

Общие правила:
- По умолчанию все изображения сохраняются в папку `images`, если явно не указано иное.
- Поддерживаемые расширения файлов для публикации: .jpg, .jpeg, .png, .gif, .bmp, .webp.
- Ограничение размера файла при публикации: 20 MB (переменная в auto_publish_photos.py MAX_FILE_SIZE = 20_000_000).

4.1 auto_publish_photos.py — автоматическая публикация фото в Telegram-канал
- Что делает: перебирает изображения в указанной папке и публикует их в канал через бота с заданным интервалом.
- Аргументы:
  - --token — токен Telegram-бота (обязательный)
  - --chat_id — chat_id или username канала (обязательный), например @my_channel или -1001234567890
  - --photos_dir — папка с фотографиями (обязательный)
  - --interval — интервал в секундах между публикациями (по умолчанию 4 часа)
- Пример запуска:

```bash
python auto_publish_photos.py --token "1234:ABCD..." --chat_id "@my_channel" --photos_dir images --interval 3600
```

- Поведение:
  - Скрипт работает в бесконечном цикле, если не прервать (Ctrl+C).
  - Игнорирует файлы больше 20 MB с сообщением в консоль.
  - Перед публикацией перемешивает порядок файлов (random.shuffle).

4.2 fetch_nasa_apod.py — скачать APOD фотографии NASA
- Что делает: скачивает n последних APOD-изображений.
- Аргументы:
  - --api_key — ваш NASA API ключ (обязательный)
  - --count — количество фото (по умолчанию 5)
  - --save_folder — папка для сохранения (по умолчанию images)
- Пример:

```bash
python fetch_nasa_apod.py --api_key YOUR_NASA_API_KEY --count 5 --save_folder images
```

- Выход: файлы nasa_apod1.jpg, nasa_apod2.jpg и т.д. в указанной папке.

4.3 fetch_nasa_epic.py — скачать EPIC фотографии NASA
- Что делает: получает метаданные EPIC, строит ссылки и скачивает изображения.
- Аргументы:
  - --api_key — ваш NASA API ключ (обязательный)
  - --count — количество фото (по умолчанию 5)
  - --save_folder — папка для сохранения (по умолчанию images)
- Пример:

```bash
python fetch_nasa_epic.py --api_key YOUR_NASA_API_KEY --count 5 --save_folder images
```

- Выход: файлы epic_01.png, epic_02.png и т.д.

4.4 fetch_spacex_images.py — скачать фотографии SpaceX
- Что делает: делает GET к переданному API URL запуска SpaceX, извлекает links.flickr.original и скачивает все ссылки.
- Аргументы:
  - --api_url — URL API SpaceX для конкретного запуска (обязательный)
  - --save_folder — папка для сохранения (по умолчанию images)
- Пример (последний запуск можно получить на API SpaceX или указать конкретный запуск):

```bash
python fetch_spacex_images.py --api_url YOUR_NASA_API_KEY --save_folder images
```

- Выход: spacex1.jpg, spacex2.jpg и т.д.

4.5 telegram_bot_check.py — проверка отправки фото в Telegram
- Что делает: читает переменные окружения (через python-dotenv) и отправляет одну фотографию в канал/чат.
- Ожидаемые переменные окружения (в .env):
  - TELEGRAM_TOKEN — токен бота
  - TG_CHAT_ID — chat id или username канала
  - TG_PHOTO_PATH — путь к фото для отправки (по умолчанию default.jpg)
- Запуск:

```bash
python telegram_bot_check.py
```

- Ожидаемый вывод в консоли: "Картинка <path> отправлена в канал!" или сообщение об ошибке.

4.6 image_downloader.py — утилита для скачивания изображений
- Функции:
  - download_image(url, save_path) — скачивает изображение и сохраняет в save_path (создаёт папку при необходимости).
  - get_file_extension(url) — возвращает расширение файла по URL.
- Используется во всех fetch_* скриптах.

5) Проверка результата и типичные ошибки
- Ошибка при запросе API (requests.exceptions.RequestException):
  - Проверьте интернет, корректность URL, корректность API ключа.
- Ошибка при сохранении файлов (OSError, PermissionError):
  - Проверьте права на папку, путь, наличие свободного места.
- Ошибка Telegram (telegram.error.TelegramError):
  - Проверьте токен бота, chat_id. Для публичных каналов chat_id выглядит как @channelname или -100… для приватных.
- Файлы не публикуются — убедитесь, что размер <20MB и расширение поддерживается.
- Если скрипт висит или зависает — проверьте таймауты сетевых запросов и доступность API.




