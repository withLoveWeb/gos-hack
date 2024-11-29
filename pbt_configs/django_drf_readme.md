# projectname

## About
<!-- Yor description here -->

## Stack:
* Django
* GraphQL
* PostgreSQL
* Docker + Docker-compose
* Gunicorn
---

## For first start
```bash
./deploy.sh local 
cd server
```
1. if set up with django container 
```bash
docker compose up
```


2. if set up only database
```bash
docker compose up db
./manage.sh run
```

### Environment variables
* `SECRET_KEY` - Django secret key. For generate new once, you can use service https://djecrety.ir/
* `DEBUG` - Flag to tell django work on debug mode or not.
* `DB_NAME` - PostgreSQL db name.
* `DB_USER` - PostgreSQL db user.
* `DB_PASSWORD` - PostgeSQL db password.


For migrate:
```bash
./manage.sh migrate
```

For create new django app:
```bash
./manage.sh app
```

It will create new django app with this structure:
```
app/
├── admin
│   └── __init__.py
├── apps.py
├── __init__.py
├── models
│   └── __init__.py
├── schema
│   ├── __init__.py
│   └── schema.py
└── services
    └── __init__.py
```
Dump graphql schema:
```bash
./manage.sh gql
```


Create superuser:
```bash
./manage.sh su
```

Open http://localhost:8000 you will see this and this is normall. There is no builded webclient.

Open http://localhost:8000/admin to see admin dashboard. Open http://localhost:8000/api to see graphql api sandbox.

### Deploy
For deploy run:
```bash
deploy.sh prod
```

On local machine app will running on http://0.0.0.0/


&copy; Fork from [PBD](https://lyaguxafrog/python-backend-devcontainers) with 💚
