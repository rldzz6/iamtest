from pydantic import BaseModel, validator
from typing import Dict, Any

class Group(BaseModel):
    group_id: str | None = None
    group_name: str | None = None
    remark: str | None = None
    search: str | None = None
    keyword: int | None = None

class Permission(BaseModel):
    group_id: str | None = None
    group_name: str | None = None
    service_id: str | None = None
    resource_id: str | None = None
    permission_id: str | None = None
    permission_name: str | None = None
    permission: str | None = None
    employee_id: str | None = None
    employee_name: str | None = None
    keyword: str | None = None

class Allocation(BaseModel):
    group_id: str | None = None
    employee_list: str | None = None
    permission_list: str | None = None