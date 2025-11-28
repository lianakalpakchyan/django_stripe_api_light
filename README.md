# Shop API

A simple Django + Stripe shop project running in Docker.  
It lets you browse items, create orders, add items, apply discounts/taxes, and pay using Stripe Checkout.

---

## How to Run

1. Make your own `.env` file based on `.env.example`.

2. Create and activate virtual environment

3. Install dependencies

```
pip install -r requirements.txt
```

4. Manage migrations

```
python manage.py migrate
```

5. Fill database

```
python fill_db.py 
```

6. Create a superuser
``` 
python manage.py createsuperuser
```

7. Run

```
python manage.py runserver
```

This will automatically:
- install dependencies  
- run migrations  
- fill the database with sample data  
- start the server on **http://localhost:8000**


