# QRkot_spreadseets

## :page_with_curl: Описание
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

<details>
<summary>:mag: Спойлер</summary>
  
![image](https://i.pinimg.com/originals/52/43/e6/5243e62fc5e182e2a9e262eeb6325d5f.gif)

</details>

### Проекты
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
Реализованы отчеты на гугл диск.

<details>
<summary>:mag: Спойлер</summary>
  
  ![image](https://github.com/user-attachments/assets/71578eaf-5210-447b-87f1-b7110f1dfdb4)

</details>

### Пожертвования
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Пользователи
Целевые проекты и отчеты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.


## :computer: Стек технологий
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![SQLAlchemy](https://camo.githubusercontent.com/002ee4ca516670df2b07f9fead4c132c71b7f367002ab21681a686c923c0acd6/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f73716c616c6368656d792d6662666266623f7374796c653d666f722d7468652d6261646765)
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- ![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)
- ![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)

## :page_with_curl: Как воспользоваться проектом
### Подготовка проекта
<details>
<summary>:mag: Спойлер</summary>

1. Клонирование проекта с GitHub
```
https://github.com/elikman/QRkot_spreadsheets.git
```
2.	Создайте виртуальное окружение.

Linux
```commandline
python3 -m venv venv
```
Windows
```commandline
python -m venv venv
```
3.	Активируйте виртуальное окружение.

Linux
```commandline
source venv/bin/activate
```
Windows
```commandline
source venv/Scripts/activate
```
4.	Установите зависимости.
```commandline
pip install -r requirements.txt
```
5.	Создать миграции и применить их.
```commandline
alembic init --template async alembic
alembic revision --autogenerate -m "Your description" --rev-id 01
alembic upgrade head
```

</details>

### Работа с проектом
Запуск проекта
```commandline
uvicorn app.main:app --reload
```
Просмотр документации
```commandline
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```
