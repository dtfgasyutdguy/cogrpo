# -*- coding: utf-8 -*-
import json
import typing as t

if t.TYPE_CHECKING:
    from pydantic import BaseModel


#         data_json_from_dicts = json.dumps(data, default=lambda x: vars(x))
def safe_model_dump(data: "BaseModel") -> dict:
    """Safe pydantic model dump."""
    try:
        return data.model_dump()
    except TypeError:

        data = json.loads(data_json_from_dicts)
    return data
