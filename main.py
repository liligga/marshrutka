import os
import pathlib
from typing import Union

import aioredis
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi_admin.app import app as admin_app
from fastapi_admin.depends import get_resources
from fastapi_admin.exceptions import (forbidden_error_exception,
                                      not_found_error_exception,
                                      server_error_exception,
                                      unauthorized_error_exception)
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Field, Link
from fastapi_admin.resources import Model as ModelResource
from fastapi_admin.template import templates
from fastapi_admin.widgets import displays
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR)
# from schemas import Driver_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from inputs import InputWithMap
from models import Admin, Driver, Driver_Pydantic, Route, Route_Pydantic

BASE_DIR = pathlib.Path(__file__).parent.resolve()
login_provider = UsernamePasswordProvider(
    admin_model=Admin
)
load_dotenv()



app = FastAPI()

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


app.mount("/admin", admin_app)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR/"static"),
    name="static",
)

print(templates.env.globals)

@app.get("/")
async def drivers_list():
    """Показываем всех водителей"""
    return await Driver_Pydantic.from_queryset(Driver.all())


@app.get("/drivers")
async def driver_by_bus(bus: int = 1):
    """Показываем всех водителей, которые работают
    на одном маршруте
    запрос будет выглядеть /drivers?bus=3
    """
    return await Driver_Pydantic.from_queryset(Driver.filter(routes__number=bus))


@app.get("/drivers/{driver_id}")
async def driver_details(driver_id: int):
    """Показываем одного водителя, по id, id передается в пути"""
    driver = await Driver_Pydantic.from_queryset_single(Driver.get(id=driver_id))
    return driver


# @app.put("/drivers")
# async def update_coordinates(driver: Driver_Pydantic):
#     """меняем координаты одного водителя, все данные(в том числе id)
#     в теле запорса."""
#     # Чтобы получить значение например поля id - обращаемся к driver.id
#     try:
#         driver_obj = list(filter(lambda d: d.get('id') == driver.id, drivers))[0]
#         driver_obj['lat'] = driver.lat
#         driver_obj['lng'] = driver.lng
#     except IndexError:
#         driver_obj = None

#     return driver_obj

register_tortoise(
    app,
    db_url=os.getenv('DATABASE_URL'),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@admin_app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@admin_app.register
class Drivers(ModelResource):
    label = "Маршруты"
    model = Route
    page_pre_title = "Список маршрутов"
    page_title = "Маршруты"
    fields = [
        "number",
        Field(
            name="path",
            label="путь",
            display=displays.InputOnly(),
            input_=InputWithMap()
        )
    ]


@admin_app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
        },
    )
