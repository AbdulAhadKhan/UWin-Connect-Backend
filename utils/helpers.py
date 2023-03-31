
import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId

'''
The following code is taken from https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
All credit goes to the original author.
'''
def form(cls: Type[BaseModel]):
    parameters = []

    for _, field in cls.__fields__.items():
        parameters.append(inspect.Parameter(
            name=field.alias,
            default=Form(...) if field.required else Form(None),
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            annotation=field.outer_type_))

    async def as_form(**data):
        return cls(**data)

    signature = inspect.signature(as_form)
    signature = signature.replace(parameters=parameters)

    as_form.__signature__ = signature
    setattr(cls, 'as_form', as_form)

    return cls


class ObjectID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")
