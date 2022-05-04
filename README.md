# Foodgram

User-friendly platform where anyone can post recipes, add them to favourites
or even form a shopping list with the needed ingredients to cook the dishes.

### Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT
- Docker
- NGINX

### How to start the app
- Go to infra folder and create .env file that should have values for the
following constants. Here's an example:
```
SECRET_KEY=<SECRET_KEY>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
- After creating the file start docker-compose:
```
sudo docker-compose up -d --build
```
- Then collect static files:
```
docker-compose exec backend python manage.py collectstatic --no-input
```
- After make migrations to sync django models with db tables:
```
docker-compose exec backend python manage.py migrate --noinput
```
- Fill the db with ingredients:
```
docker-compose exec backend python manage.py load_ingredients
```

Author: [techinek](https://github.com/Techinek)
-12