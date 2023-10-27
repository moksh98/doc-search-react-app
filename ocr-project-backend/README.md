# OCR Project Backend

## Setup

### Create `.env` file (ask for creds from owner)
```
SECRET_KEY = <>
PASSWORD = <>

S3_ACCESS_KEY_ID = <>
S3_SECRET_ACCESS_KEY = <>

DB_URL = <>
DB_PORT = 5432
DATABASE = <>
DB_USER = <>
DB_PASS = <>

PDF_S3_BUCKET = <>

ES_HOST = <>
ES_USER = <>
ES_PASS = <>
```

### Virtualenv
Create: 
```shell
python3 -m venv kcldsdev
```

Activate: 
```shell
source kcldsdev/bin/activate
```

Install requirements: 
```shell
pip3 install -r requirements.txt
```

Deactivate: 
```shell
deactivate
```

## Postgres Migrations

### Enable CIText extension
Run this query on your postgres database the first time you create it
```sql
CREATE EXTENSION citext;
```
### Create migrations
```shell
alembic revision -m "your message"
```
### Run Migrations
```shell
alembic upgrade head
```

## Run Server

### FastAPI
```shell
uvicorn app.main:fastapi --reload
```

### Celery
```shell
celery -A app.core.celery_app.celapp worker --loglevel=INFO
```
