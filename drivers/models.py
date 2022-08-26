import datetime

from fastapi_admin.models import AbstractAdmin
from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from .fields import PathField


class Route(Model):
    number = fields.IntField()
    path = PathField()


class Driver(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    routes = fields.ManyToManyField("models.Route")


class Admin(AbstractAdmin):
    last_login = fields.DatetimeField(description="Last Login", default=datetime.datetime.now)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}#{self.username}"

Tortoise.init_models(["__main__"], "models")

Driver_Pydantic = pydantic_model_creator(Driver)
Route_Pydantic = pydantic_model_creator(Route)