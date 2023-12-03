from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class response(BaseModel):
    message: str
    data: List[dict[str, Any]]