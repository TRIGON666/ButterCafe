# ButterCafe

Сайт кафе ButterCafe на Django с PostgreSQL.

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
```

2. Активируйте виртуальное окружение:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта и добавьте следующие переменные:
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=buttercafe
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

5. Создайте базу данных PostgreSQL с именем buttercafe

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

```
buttercafe/
├── manage.py
├── requirements.txt
├── .env
├── buttercafe/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── cafe/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── static/
    │   ├── css/
    │   ├── js/
    │   └── images/
    └── templates/
        ├── base.html
        ├── home.html
        ├── menu.html
        ├── cart.html
        └── admin/
            └── dashboard.html
``` 