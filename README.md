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

## Admin

- Username: `admin`
- Password: `anupam@vaikom`

API: `http://127.0.0.1:8000/api/`  
Django admin: `http://127.0.0.1:8000/django-admin/`
