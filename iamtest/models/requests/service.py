from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Service(BaseModel):
    service_id: str | None = None
    service_name: str | None = None
    service_url: str | None = None