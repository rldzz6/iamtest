from pydantic import BaseModel, validator
from typing import Dict, Any

class Permission(BaseModel):
    permission_id: str | None = None
    service_id: str | None = None
    resource_id: str | None = None
    permission_name: str | None = None
    permission: str | None = None
    remark: str | None = None
    search: str | None = None