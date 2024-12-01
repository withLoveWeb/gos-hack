#!/bin/bash

./manage.sh makemigrations --no-input
./manage.sh migrate --no-input
./manage.sh collectstatic --no-input

./manage.sh run
