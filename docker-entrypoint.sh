#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --no-input

# Apply database migrations
echo "Start task processor"
python manage.py process_tasks&

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
