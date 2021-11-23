# Решение тестового задания для backend-разработчиков от avito.ru

Решение [тестового задания](https://github.com/avito-tech/verticals/blob/master/trainee/backend.md) для backend-разработчиков от [avito](https://avito.ru/)

## Project setup

### Development

```shell script
pip install -r requirements.txt

alembic upgrade head
python -m application.asgi
```

### Docker

```shell script
docker-compose up -d

# Linux
x-www-browser http://localhost:8000/docs

# macOS
open http://localhost:8000/docs

# PowerShell
start http://localhost:8000/docs
```

## Unit tests

```shell script
pytest
```