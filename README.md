# 🚀 MinIO Upload Backend

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

Проект для загрузки файлов через FastAPI + MinIO в публичное облако с возможностью отдачи публичных ссылок.

---

## 🛠️ Используемые технологии
- **FastAPI**: современный веб-фреймворк для создания API на Python.
- **MinIO**: высокопроизводительное решение для хранения объектов, совместимое с Amazon S3.
- **Docker**: платформа для автоматизации развертывания приложений в контейнерах.
- **Docker Compose**: инструмент для определения и запуска многоконтейнерных Docker приложений.


## 📦 Быстрый старт

1. **Клонируем репозиторий:**
   ```bash
   git clone https://github.com/macalistervadim/upload_images
   cd upload_images


2. **Создаем файл `.env` в корне проекта:**
   ```bash
   cp .env.example .env
   ```

3. **Запускаем проект:**
   ```bash
    docker-compose up -d
    ```

4. **Проверяем работу API:**
    ```bash
    curl -X POST "http://localhost:8000/upload" -F "file=@path/to/your/file.jpg"
    ```
   
5. **Сервисы:**
    - **FastAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **MinIO**: [http://localhost:9000](http://localhost:9000) (логин: `из .env`, пароль: `из .env`)

## Как пользоваться API
1. **Загрузка файла:**
   - Метод: `POST`
   - URL: `/upload`
   - Параметры:
     - `file`: файл для загрузки
   - Ответ:
     ```json
     {
       "url": "https://your-minio-url/bucket-name/file-name"
     }
     ```
   Пример запроса через curl:
   ```bash
   curl -X 'POST' \
     'http://<your-server-ip>:8000/upload/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@yourfile.jpg'
   ```
   Ответ:
    ```json
   {
        "url": "http://<your-server-ip>:9000/images/yourfile.jpg"
    }
    ```

## 📄 Лицензия
Этот проект лицензирован под MIT License. Пожалуйста, ознакомьтесь с файлом [LICENSE](LICENSE) для получения подробной информации.

## 📧 Контакты
Если у вас есть вопросы или предложения, не стесняйтесь обращаться в **[issues](https://github.com/macalistervadim/upload_images/issues)**

