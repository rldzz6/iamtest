from pydantic import BaseModel
from typing import List, Optional

class Permission(BaseModel):
    permission_id: int
    service_id: int | None = None
    resource_id: int | None = None
    permission_name: str | None = None
    permission: int | None = None
    remark: str | None = ''

class User(BaseModel):
    employee_id: str | None = None
    employee_name: str | None = None
    permission_id: int | None = None
    permission_name: str | None = None
    permission: int | None = None
    group_id: int | None = None
    group_name: str | None = None