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
    employee_list: Any | None = []
    permission_list: Any | None = []

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

class Log(BaseModel):
    group_id: str = '그룹 ID'
    group_name: str = '그룹명'
    permission_id: str = '권한 ID'
    service_id: str = '서비스 ID'
    resource_id: str = '리소스 ID'
    permission_name: str = '권한명'
    permission: str = '권한'
    remark: str = '비고'
    keyword: str = '검색어'
    employee_id: str = '사원번호'
    employee_list : str = '허용 사원 목록'
    permission_list : str = '허용 권한 목록'
    group_list : str = '권한 그룹 목록'