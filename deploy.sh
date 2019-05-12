#!/bin/sh

celery -A app.celery worker --detach
gunicorn app:app --bind 0.0.0.0:${PORT}
