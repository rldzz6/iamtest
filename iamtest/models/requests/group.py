from pydantic import BaseModel, validator
from typing import Dict, Any

class Group(BaseModel):
    group_id: str | None = None
    group_name: str | None = None
    remark: str | None = None
    keyword: str | None = None

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
    employee_list: Any | None = None
    permission_list: Any | None = None

    @validator('permission_list')
    def permission_to_list(cls, permission_list):
        if permission_list == None or permission_list == '':
            return ''
        return permission_list.replace(' ', '').split(',')
    @validator('employee_list')
    def group_to_list(cls, employee_list):
        if employee_list == None or employee_list == '':
            return ''
        return employee_list.replace(' ', '').split(',')

class User(BaseModel):
    employee_id: str | None = None
    permission_id: str | None = None
    group_id: str | None = None