from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Service(BaseModel):
    service_id: str | None = ''
    service_name: str | None = ''
    service_url: str | None = None
    search: str | None = None
    
    @validator('search')
    def param_init(param):
        return '%' + param + '%'