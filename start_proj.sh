#!/bin/bash

# Start Redis server
echo "Starting Redis server =3 ==3 ===3 ====3"
redis-server --port 6379 &

echo "Starting Celery worker =3 ==3 ===3 ====3"
celery -A its_backend worker -l info &
# Start Django development server
echo "Starting Django development server =3 ==3 ===3 ====3"
python manage.py runserver
