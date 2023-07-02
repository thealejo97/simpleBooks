# Docker by Alejandro Montaño
FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DIR /simpleBooks_backend

RUN mkdir $DJANGO_DIR

# Actualizamos pip
RUN pip3 install --upgrade pip

# Actualizamos repositorios e instalamos nano y git
RUN apt-get update \
    && apt-get install -y nano git

WORKDIR $DJANGO_DIR

# Copiamos los requeriments
COPY ./requeriments.txt $DJANGO_DIR/requeriments.txt

# Instalamos los requeriments
RUN pip3 install -r $DJANGO_DIR/requeriments.txt

# Copiamos el proyecto
COPY . .

# Ejecutamos las migraciones
RUN python manage.py migrate

EXPOSE 8000