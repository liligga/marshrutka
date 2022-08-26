import os
import pathlib

import aioredis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_admin.providers.login import UsernamePasswordProvider
from starlette.staticfiles import StaticFiles
# from schemas import Driver_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from admin import admin_app
from drivers import Admin, apishka

##### SOME CONSTANTS AND ENV VARS #####
BASE_DIR = pathlib.Path(__file__).parent.resolve()
load_dotenv()
########################################
############## MAIN APP ################
app = FastAPI()
########################################
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(os.getenv('REDIS_URL'), max_connections=10)
    await admin_app.configure(
        admin_path='/admin',
        template_folders=[BASE_DIR/"templates"],
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
            )
        ],
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








