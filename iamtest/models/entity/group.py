from pydantic import BaseModel
from typing import List

class Group(BaseModel):
    group_id: int
    group_name: str | None = None
    remark: str | None = None
    

class Group_Permission(BaseModel):
    id: int
    group_id: int
    permission_id: int
