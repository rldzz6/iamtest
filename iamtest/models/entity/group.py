from pydantic import BaseModel
from typing import NamedTuple

class Group(NamedTuple):
    group_id: int
    group_name: str | None = None
    remark: str | None = None

class Permission(NamedTuple):
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
    employee_rank: str | None = None

class Model(BaseModel):
    group: Group | None = None
    permission: Permission | None = None