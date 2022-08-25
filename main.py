from typing import Union
from fastapi import FastAPI
# from database import drivers
from models import (
    Driver_Pydantic,
    Route_Pydantic,
    Driver,
    Route
)
# from schemas import Driver_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI()



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
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)