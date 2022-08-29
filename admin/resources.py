
from fastapi_admin.app import app as admin_app
from fastapi_admin.resources import Field, Link
from fastapi_admin.resources import Model as ModelResource
from fastapi_admin.template import templates
from fastapi_admin.widgets import displays

from drivers.models import Driver, Route

from .inputs import InputWithMap


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
            # display=displays.InputOnly(),
            input_=InputWithMap()
        )
    ]
