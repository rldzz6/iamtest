from pydantic import BaseModel
from typing import NamedTuple

class Employee(NamedTuple):
    employee_id: str
    employee_name: str
    employee_mail: str | None = None
    employee_rank: str | None = None

class Model(BaseModel):
    data: Employee