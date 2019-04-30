#!/usr/bin/env bash

celery -A app.celery worker --detach
flask run --host=0.0.0.0