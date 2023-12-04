from pydantic import BaseModel
from typing import Dict, Any, List

class response(BaseModel):
    code: str | None = ''
    message: str | None = ''
    data: List[dict[str, Any]] | None = []