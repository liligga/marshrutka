from tortoise import Tortoise, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from fields import PathField


class Route(Model):
    number = fields.IntField()
    path = PathField()


class Driver(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    routes = fields.ManyToManyField("models.Route")


Tortoise.init_models(["__main__"], "models")

Driver_Pydantic = pydantic_model_creator(Driver)
Route_Pydantic = pydantic_model_creator(Route)