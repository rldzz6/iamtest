from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Service(BaseModel):
    service_id: str | None = None
    service_name: str | None = None
    service_url: str | None = None
    search: str | None = None
    keyword: str | None = None