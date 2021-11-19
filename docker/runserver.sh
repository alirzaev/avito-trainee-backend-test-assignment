#!/bin/sh

alembic upgrade head
uvicorn application.main:application --port 80 --host 0.0.0.0
