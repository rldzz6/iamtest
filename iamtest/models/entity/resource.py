from pydantic import BaseModel
from typing import NamedTuple

class Resource(NamedTuple):
    resource_id: int | None = None
    resource_name: str | None = None
    remark: str | None = None
    service_id: int | None = None
    service_name: str | None = None

class Model(BaseModel):
    data: Resource