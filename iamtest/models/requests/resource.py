from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Resource(BaseModel):
    resource_id: str | None = None
    service_id: str | None = None
    resource_name: str | None = None
    remark: str | None = None
    keyword: str | None = None