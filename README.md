# gos-hack

## About
Это решение Хакатона Hack&Change 2024 от команды **РосГосХак**.
Трек: Web/DA: Сервис заказов речного шеринг-такси от Правительства Москвы.


## Stack:
* Django
* Redis
* PostgreSQL
* Docker + Docker-compose


## For first start

* cd ./gos-hack
* touch .env
* в папке ./gos-hack/server/.env.example пиведен пример заполнения .env
* cp .env server/.env
* docker compose up —build



Open http://localhost:8000

Open http://localhost:8000/admin to see admin dashboard.

