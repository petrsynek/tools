import pydantic

from typing import Type, Any

class Mixin:

    def print(self):
        print(self.field)

class Base(pydantic.BaseModel, Mixin):

    field: str
    other: Type[object]

    # class Config:
    #     allow_mutation = False
    #     use_enum_values = True
    #     extra = pydantic.Extra.forbid



a = Base(field = "asdfasdf", other="asdfadf")
print(a)
a.print()