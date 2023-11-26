from pydantic import BaseModel
from typing import List, Optional

class Service(BaseModel):
    service_id: int
    service_name: str
    service_url: Optional[str] = None
