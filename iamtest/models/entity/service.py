from pydantic import BaseModel
from typing import NamedTuple

class Service(NamedTuple):
    service_id: int
    service_name: str | None = None
    service_url: str | None = None

class Model(BaseModel):
    data: Service