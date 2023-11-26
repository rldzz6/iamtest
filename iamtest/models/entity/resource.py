from pydantic import BaseModel
from typing import List, Optional

class Resource(BaseModel):
    resource_id: int
    service_id: int | None = None
    name: str | None = None
    remark: str | None = None