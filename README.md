# QRkot

![Python](https://img.shields.io/badge/python-3670A0?logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?logo=sqlite&logoColor=white)
---

Это учебный проект на базе фреймворка **FastAPI**. 

QRKot — приложение для Благотворительного фонда поддержки котиков.
Фонд собирает пожертвования на различные целевые проекты: на медицинское 
обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в 
подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные 
с поддержкой кошачьей популяции :)

### Проекты
Администратор может создать несколько целевых проектов, с указанием 
необходимой суммы. После сбора необходимой суммы, проект закрывается. Все 
проекты доступны для просмотра без авторизации.
### Пожертвования
Зарегистрированные пользователи могут вносить пожертвования. Все пожертвования 
идут на обеспечение проектов в порядке очереди. Пользователь может видеть 
только свои пожертвования.
### Отчёт
Приложение умеет формировать отчёт в гугл-таблице, в котором перечислены 
закрытые проекты, отсортированные по скорости сбора средств.

## Стек технологий:
- Python 3.9
- FastAPI v.0.78.0
- SQLite
- SQLAlchemy
- Alembic
- Google API


## Подготовка к работе:

<details>
    <summary><b>Клонируйте репозиторий</b></summary>

```shell
git clone https://github.com/elikman/QRkot_spreadsheets.git

cd qrkot_spreadsheets
```
</details>

<details>
    <summary><b>Создайте файл <code>.env</code> в корне проекта 
со своими данными</b></summary>

```dotenv
APP_TITLE=Кошачий благотворительный фонд (0.1.0)
DESCRIPTION=Сервис для поддержки котиков!
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=QU:=r6S7+{'et=rf
FIRST_SUPERUSER_EMAIL=superuser@example.com
FIRST_SUPERUSER_PASSWORD=5>~H*d&:Yz5jXrna
# Доступ к сервисному аккаунту Google Cloud Platform
EMAIL=
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
```
> Данные для доступа к сервисному аккаунту Google Cloud Platform возьмите из
> `*.json` файла, полученного после создания аккаунта.
</details>

<details>
    <summary><b>Создайте и активируйте виртуальное окружение</b></summary>

```shell
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip

# Windows
python -m venv venv
source venv/scripts/activate
python -m pip install --upgrade pip
```
> В проекте используется **Python** версии **3.9**
</details>

<details>
    <summary>
        <b>Установите зависимости из файла <code>requirements.txt</code></b>
    </summary>

```shell
pip install -r requirements.txt
```
</details>

<details>
    <summary><b>Примените миграции</b></summary>

```shell
alembic upgrade head
```
</details>

<details>
    <summary><b>Запустите программу</b></summary>

```shell
uvicorn app.main:app --reload
```
> По-умолчанию приложение запускается на 8000 порту, но вы можете изменить 
> порт: `--port 8001`
</details>


## Документация
После запуска программы документация будет доступна по адресам:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
