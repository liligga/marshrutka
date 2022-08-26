from fastapi import FastAPI

from .models import Admin, Driver, Driver_Pydantic, Route, Route_Pydantic

###### APP ######
apishka = FastAPI()

@apishka.get("/")
async def drivers_list():
    """Показываем всех водителей"""
    return await Driver_Pydantic.from_queryset(Driver.all())


@apishka.get("/drivers")
async def driver_by_bus(bus: int = 1):
    """Показываем всех водителей, которые работают
    на одном маршруте
    запрос будет выглядеть /drivers?bus=3
    """
    return await Driver_Pydantic.from_queryset(Driver.filter(routes__number=bus))


@apishka.get("/drivers/{driver_id}")
async def driver_details(driver_id: int):
    """Показываем одного водителя, по id, id передается в пути"""
    driver = await Driver_Pydantic.from_queryset_single(Driver.get(id=driver_id))
    return driver


# @apishka.put("/drivers")
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
