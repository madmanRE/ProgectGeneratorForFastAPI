# ProgectGenerator

***A lightweight template for a project on the FastAPI framework.***

___

### Contains

* Main app
* App structure (models, schemas, routers)
* Caching with Redis
* Authorization with fastapi_users
* Database async connector for postgres
* Migrations feature with Alembic
* Tests
* Module *black* for PEP8
* Dockerfile and docker-compose for App, Postgres and Redis
* AdminPanel with SqlAdmin

___

### Structure

```commandline
.
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   └── auth
│   │   ├── __init__.py
│   │   ├── auth_config.py
│   │   └── manager.py
│   └── models
│   │   ├── __init__.py
│   │   └── models.py
│   └── routers
│   │   ├── __init__.py
│   │   └── auth_router.py
│   └── test
│   │   ├── __init__.py
│   │   └── auth_tests.py
│   └── schemas
│       ├── __init__.py
│       └── schemas.py
```

___


