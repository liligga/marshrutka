import re
from typing import Tuple, Type

from tortoise import ConfigurationError
from tortoise.fields import Field


class PathField(Field):
    SQL_TYPE = "PATH"


    @staticmethod
    def _convert_to_tuple(val: str) -> Tuple:
        split_pattern = r'\)\,\s?\('
        val_copy = val.lstrip('(')
        val_copy = val_copy.rstrip(')')
        lst = re.split(split_pattern, val_copy)
        result = []
        for x in lst:
            s = x.split(',')
            s = tuple(map(float ,s))
            result.append(s)
        return tuple(result)

    @staticmethod
    def _convert_to_tuple_v2(val: str) -> Tuple:
        return tuple((point.x, point.y) for point in val.points)

    def to_db_value(self, value: Tuple, instance) -> str:
        return str(value)

    def to_python_value(self, value: str) -> Tuple:
        if isinstance(value, tuple):
            return value
        try:
            result = PathField._convert_to_tuple(value)
            return result
        except (ValueError, AttributeError) as error:
            return tuple()        
