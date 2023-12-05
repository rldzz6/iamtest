from pydantic import BaseModel
from typing import List, Optional

class Employee(BaseModel):
    employee_id: str
    employee_name: str | None = None
    employee_email: str | None = None
    rank: str | None = None
