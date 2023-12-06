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
    group_name:  str | None = None
    employee_id:  str | None = None
    employee_name:  str | None = None
    page_no: int | None = 0
    
    @validator('page_no')
    def page_init(page_no):
        page_no -= 1
        return page_no;