FROM python:3.11.5-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && \
    apk add --no-cache \
    build-base \
    python3-dev \
    libffi-dev \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    jpeg-dev \
    zlib-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    bash \
    font-noto \
    && rm -rf /var/cache/apk/*

RUN apk update \
    && apk add --no-cache  \
    gcc  \
    musl-dev  \
    postgresql-dev  \
    python3-dev  \
    libffi-dev  \
    freetype-dev \
    && apk add openjdk11 \
    && pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

# Copia el archivo .env desde el proyecto al contenedor
COPY .env /app/.env

# Carga las variables de entorno desde el archivo .env
RUN set -a && . /app/.env && set +a

# Exponer el puerto donde correrá FastAPI
EXPOSE 5003

# Comando para iniciar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003", "--reload"]
