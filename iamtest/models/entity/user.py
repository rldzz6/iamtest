from pydantic import BaseModel
from typing import Dict, Any

class Employee(BaseModel):
    employee_id: str
    employee_name: str
    employee_mail: str | None = None
    employee_rank: str | None = None