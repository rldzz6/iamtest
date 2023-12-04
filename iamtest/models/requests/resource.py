from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Resource(BaseModel):
    resource_id: str | None = None
    service_id: str | None = None
    name: str | None = None
    remark: str | None = None
    search: str | None = None