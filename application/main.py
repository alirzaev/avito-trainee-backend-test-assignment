import uvicorn
from fastapi import FastAPI

from .config import get_config
from .routers import ad

config = get_config()

application = FastAPI(
    debug=config.DEBUG,
    title='Ad service',
    description='A service for storing and submitting ads'
)
application.include_router(ad.router)


if __name__ == '__main__':
    uvicorn.run(application, port=8000, debug=config.DEBUG)
