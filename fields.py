from typing import Type, Tuple

from tortoise import ConfigurationError
from tortoise.fields import Field


class PathField(Field):
    SQL_TYPE = "PATH"

    def _convert_to_tuple(val: str) -> Tuple:
        val_copy = val.lstrip('(')
        val_copy = val_copy.rstrip(')')
        lst = val_copy.split('), (')
        result = []
        for x in lst:
            s = x.split(',')
            s = tuple(map(float ,s))
        return tuple(result)

    def to_db_value(self, value: Tuple, instance) -> str:
        return str(value)

    def to_python_value(self, value: str) -> Tuple:
        try:
            return self._convert_to_tuple(value)
        except ValueError:
            return tuple()        
