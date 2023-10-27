Alembic is a database migration tool used in SQLAlchemy. It is used to manage and track changes to your database schema over time. This documentation provides a step-by-step guide on how to set up Alembic, how to use it, and the various functionalities it provides.

## Prerequisites
- Python 3.x
- SQLAlchemy
- SQL database (e.g. PostgreSQL, MySQL)
- Installation

## Alembic can be installed using pip:

```bash
pip install alembic
```

## Initialize an Alembic project in your working directory:
```csharp
alembic init alembic
```

This will create a new directory named alembic in your working directory, with the following structure:
```markdown
alembic/
    alembic.ini
    env.py
    scripts/
        __init__.py
        version_script.py
```
The alembic.ini file contains the configuration information for Alembic, including the database URL and the location of the migrations.

The env.py file contains the environment information and is used to configure SQLAlchemy.

The scripts directory contains the actual Alembic migration scripts.

## Creating the First Migration
To create the first migration, use the following command:
```python
alembic revision --autogenerate -m "Initial revision"
```

This will generate a new file in the scripts directory with the latest schema information from your database.

Review the generated file to ensure it accurately reflects the desired changes to your schema.

## Upgrading and Downgrading the Database
### To upgrade the database, use the following command:
```bash
alembic upgrade head
```

This will apply the latest schema changes to your database.

### To downgrade the database, use the following command:
```bash
alembic downgrade -1
```

## To generate SQL query based output use --sql
```bash
alembic upgrade head --sql
```

This will give the corresponding sql queries that will be executed when  ```bash alembic upgrade head``` is executed

