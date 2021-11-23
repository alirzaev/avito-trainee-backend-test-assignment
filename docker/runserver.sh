#!/bin/sh

alembic upgrade head
uvicorn application.asgi:application --port 80 --host 0.0.0.0
