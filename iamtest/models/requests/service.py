from pydantic import BaseModel, validator
from typing import Dict, Any, List

class Service(BaseModel):
    service_id: str | None = None
    service_name: str | None = None
    service_url: str | None = None
    keyword: str | None = None

class Log(BaseModel):
    service_id : str = '서비스 ID'
    service_name : str = '서비스명'
    service_url : str = '서비스 URL'
    keyword : str = '검색어'