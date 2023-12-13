from pydantic import BaseModel
from typing import Dict, Any, List

class Service(BaseModel):
    service_id: int
    service_name: str | None = None
    service_url: str | None = None
