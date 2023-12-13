from pydantic import BaseModel, validator
from typing import Dict, Any

class Permission(BaseModel):
    permission_id: str | None = None
    service_id: str | None = None
    resource_id: str | None = None
    permission_name: str | None = None
    permission: str | None = None
    remark: str | None = None
    keyword: str | None = None
    employee_id: str | None = None

    @validator('keyword')
    def keyword_init(cls, keyword):
        if keyword == '':
            return None

class User(BaseModel):
    employee_id: str | None = None
    permission_id: str | None = None
    group_id: str | None = None

class Allocation(BaseModel):
    employee_id: str | None = None
    permission_list: Any | None = None
    group_list: Any | None = None

    @validator('permission_list')
    def permission_to_list(cls, permission_list):
        if permission_list == None or permission_list == '':
            return ''
        return permission_list.replace(' ', '').split(',')
    @validator('group_list')
    def group_to_list(cls, group_list):
        if group_list == None or group_list == '':
            return ''
        return group_list.replace(' ', '').split(',')