import os
import pathlib

import aioredis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_admin.exceptions import (forbidden_error_exception,
                                      not_found_error_exception,
                                      server_error_exception,
                                      unauthorized_error_exception)
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.staticfiles import StaticFiles
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR)
# from schemas import Driver_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from admin import admin_app
from drivers import Admin, apishka

##### SOME CONSTANTS AND ENV VARS #####
BASE_DIR = pathlib.Path(__file__).parent.resolve()
login_provider = UsernamePasswordProvider(
    admin_model=Admin
)
load_dotenv()
########################################
############## MAIN APP ################
app = FastAPI()
########################################
@app.on_event("startup")
async def startup():
    admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
    admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

    redis = await aioredis.from_url(os.getenv('REDIS_URL'), max_connections=10)
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[BASE_DIR/"templates"],
        providers=[login_provider],
        redis=redis,
        default_locale='ru'
    )

    app.mount(
        "/static",
        StaticFiles(directory=BASE_DIR/"static"),
        name="static",
    )
    app.mount("/admin", admin_app)
    app.mount("/", apishka)
    register_tortoise(
        app,
        db_url=os.getenv('DATABASE_URL'),
        modules={"models": ["drivers.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )








