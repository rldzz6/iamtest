from pydantic import BaseModel, validator
from typing import Dict, Any, List

class Service(BaseModel):
    service_id: int | None = None
    service_name: str | None = None
    service_url: str | None = None
    keyword: str | None = None