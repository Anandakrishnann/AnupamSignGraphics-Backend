# Anupam Signgraphics — Backend

Django REST API for Anupam Signgraphics (Vaikom, Kerala).

## Setup

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/`  
Django admin: `http://127.0.0.1:8000/django-admin/`

## Render

**Build command**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_data
```

**Start command** 
```bash
gunicorn config.wsgi:application
```
