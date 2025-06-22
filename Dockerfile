FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    TZ=Europe/Berlin

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone
RUN pip install --no-cache-dir poetry

WORKDIR /var/www/service-healthbot/
COPY . .
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction
RUN rm -rf ~/.cache/pypoetry

EXPOSE 7070
