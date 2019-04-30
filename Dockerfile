FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
EXPOSE 5000
CMD [￿￿"deploy.sh"]