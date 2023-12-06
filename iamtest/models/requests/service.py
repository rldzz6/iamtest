from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Service(BaseModel):
    service_id: str | None = None
    service_name: str | None = None
    service_url: str | None = None
    search: str | None = None
    page_no: int | None = 0
    
    @validator('page_no')
    def page_init(page_no):
        page_no -= 1
        return page_no;