FROM python:3.6-slim


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

COPY . /celery-app
WORKDIR /celery-app

RUN python3.6 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT celery -A tasks worker --loglevel=info
