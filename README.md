# Отчёт в Google Sheets для QRKot

## Технологии:

- Python 3.9.13
- FastAPI 0.78.0
- SQLAlchemy 1.4.36
- Alembic 1.7.7
- Uvicorn 0.17.6
- Aiogoogle 4.2.0

## Установка (Windows):

```

1. Переход в директорию QRkot_spreadsheets

```
cd QRkot_spreadsheets
```

2. Создание виртуального окружения

```
python -m venv venv
```

3. Активация виртуального окружения

```
source venv/Scripts/activate
```

4. Обновите pip

```
python -m pip install --upgrade pip
```

5. Установка зависимостей

```
pip install -r requirements.txt
```

6. Создание и настройка базы данных

```
APP_TITLE=...
APP_DESCRIPTION=...
DATABASE_URL=...
SECRET=...
FIRST_SUPERUSER_EMAIL=...
FIRST_SUPERUSER_PASSWORD=...
TYPE=...
PROJECT_ID=...
PRIVATE_KEY_ID=...
PRIVATE_KEY=...
CLIENT_EMAIL=...
CLIENT_ID=...
AUTH_URI=...
TOKEN_URI=...
AUTH_PROVIDER_X509_CERT_URL=...
CLIENT_X509_CERT_URL=...
EMAIL=...
```

7. Запуск сервера с автоматическим рестартом

```
uvicorn app.main:app --reload
```
