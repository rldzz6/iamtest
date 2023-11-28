from pydantic import BaseModel, validator
from typing import Dict, Any

class Permission(BaseModel):
    permission_id: str | None = None
    service_id: str | None = ''
    resource_id: str | None = ''
    permission_name: str | None = ''
    permission: str | None = ''
    remark: str | None = None
    search: str | None = None