from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class Response(BaseModel):
    code: str | None = ''
    message: str | None = ''
    data: List[Dict[str, Any]] | Dict[str, Any] | None = None
    total_count: int | None = 0
    total_page: int | None = 1

class Log(BaseModel):
    log_id: int | None = None
    category: str | None = None
    description: str | None = None
    action: str | None = None
    action_time: str | None = None
    employee_id: str | None = None
    ip: str | None = None

class Errorlog(BaseModel):
    identity: str | None = None
    url_path: str | None = None
    asc_time: str | None = None
    status: str | None = None
    level: str | None = None
    message: str | None = ''
