from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class response(BaseModel):
    code: str | None = ''
    message: str | None = ''
    data: List[dict[str, Any]] | None = []

class Log(BaseModel):
    id: int | None = None
    description: str | None = None
    category: str | None = None
    work_type: str | None = None
    work_time: str | None = str(datetime.now())
    employee_id: str | None = None
    work_ip: str | None = None
    work_status: int | None = None