from typing import Union
from fastapi import FastAPI
from database import drivers

from schemas import Driver_Pydantic

app = FastAPI()



@app.get("/")
def drivers_list():
    """Показываем всех водителей"""
    return drivers


@app.get("/drivers")
def driver_by_bus(bus: int = 1):
    """Показываем всех водителей, которые работают
    на одном маршруте
    запрос будет выглядеть /driver?bus=3
    """
    return list(filter(lambda d: d.get('bus') == bus, drivers))


@app.get("/drivers/{driver_id}")
def driver_details(driver_id: int):
    """Показываем одного водителя, по id"""
    try:
        driver = list(filter(lambda d: d.get('id') == driver_id, drivers))[0]
    except IndexError:
        driver = None

    return driver


@app.put("/drivers")
def update_coordinates(driver: Driver_Pydantic):
    """меняем координаты одного водителя, все данные в теле запорса"""
    try:
        driver_obj = list(filter(lambda d: d.get('id') == driver.id, drivers))[0]
        driver_obj['lat'] = driver.lat
        driver_obj['lng'] = driver.lng
    except IndexError:
        driver_obj = None

    return driver_obj