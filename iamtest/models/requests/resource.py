from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional

class Resource(BaseModel):
    resource_id: str | None = None
    service_id: str | None = None
    resource_name: str | None = None
    remark: str | None = None
    keyword: str | None = None

class Log(BaseModel):
    resource_id: str = '리소스 ID'
    service_id: str = '서비스 ID'
    resource_name: str = '리소스명'
    remark: str = '비고'
    keyword: str = '검색어'
