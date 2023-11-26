from pydantic import BaseModel, validator
from typing import Dict, Any

class Group(BaseModel):
    group_id: str | None = ''
    group_name: str | None = ''
    remark: str | None = None
    search: str | None = None
    
    @validator('search')
    def param_init(param):
        return '%' + param + '%'
    
class Group_Permission(BaseModel):
    id: str | None = ''
    group_id: str | None = '' 
    permission_id: str | None = ''