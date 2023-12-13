from pydantic import BaseModel
from typing import NamedTuple

class Permission(NamedTuple):
    permission_id: int
    permission_name: str | None = None
    permission: int | None = None
    remark: str | None = None
    resource_id: int | None = None
    resource_name: str | None = None
    service_id: int | None = None
    service_name: str | None = None

class User(NamedTuple):
    employee_id: str | None = None
    employee_name: str | None = None
    permission_id: int | None = None
    permission_name: str | None = None
    permission: int | None = None
    group_id: int | None = None
    group_name: str | None = None
    permission_type: str | None = None #P: 권한, G:그룹
    resource_id: int | None = None
    resource_name: str | None = None
    service_id: int | None = None
    service_name: str | None = None

class Model(BaseModel):
    permission: Permission | None = None
    user: User | None = None