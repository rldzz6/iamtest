from pydantic import BaseModel
from typing import List, Optional

class Resource(BaseModel):
    resource_id: int | None = None
    service_id: int | None = None
    name: str | None = ''
    remark: str | None = ''