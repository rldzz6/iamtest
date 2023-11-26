from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Resource(BaseModel):
    resource_id: int | None = ''
    service_id: str | None = ''
    name: str | None = ''
    remark: str | None = None
    search: str | None = None
    
    @validator('search')
    def param_init(param):
        return '%' + param + '%'