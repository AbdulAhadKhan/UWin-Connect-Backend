'''
The following code is taken from https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
All credit goes to the original author.
'''

import inspect
from typing import Type

from fastapi import Form
from pydantic import BaseModel

def form(cls: Type[BaseModel]):
    parameters = []

    for _, field in cls.__fields__.items():
        parameters.append(inspect.Parameter(default=Form(...) if field.required \
                                            else None, annotation=field.outer_type_))

    async def as_form(**data):
        return cls(**data)

    signature = inspect.signature(as_form)
    signature = signature.replace(parameters=parameters)

    as_form.__signature__ = signature
    setattr(cls, 'as_form', as_form)

    return cls
