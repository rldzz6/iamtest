from pydantic import BaseModel, validator
from typing import Dict, Any

class Group(BaseModel):
    group_id: str | None = None
    group_name: str | None = None
    remark: str | None = None
    search: str | None = None
    page_no: int | None = 0
    
    @validator('page_no')
    def page_init(page_no):
        page_no -= 1
        return page_no;
  
class Group_Permission(BaseModel):
    id: str | None = ''
    group_id: str | None = '' 
    permission_id: str | None = ''
    page_no: int | None = 0
        
    @validator('page_no')
    def page_init(page_no):
        page_no -= 1
        return page_no;