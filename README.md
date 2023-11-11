# Alumni Portal for MMCOE

DB Diagram: https://dbdiagram.io/d/MMCOE-Alumni-Portal-654ce8d57d8bbd6465dac5ae

## Install packages:
```
pip install -r requirements.txt
```

## .env file config (PostgreSQL):
```
DB_NAME = *****
DB_USER = *****
DB_PASS = *****
DB_HOST = *****
DB_PORT = *****
```

## Migrate to Database:
```
python manage.py migrate
```

## Run backend:
```
python manage.py runserver
```

