from pydantic import BaseModel
from typing import List

class Group(BaseModel):
    group_id: int
    group_name: str | None = None
    remark: str | None = None
    

class Permission(BaseModel):
    group_id: int | None = None
    service_id: int | None = None
    service_name: str | None = None
    resource_id: int | None = None
    resource_name: str | None = None
    permission_id: int | None = None
    permission_name: str | None = None
    permission: int | None = None
    employee_id: str | None = None
    employee_name: str | None = None