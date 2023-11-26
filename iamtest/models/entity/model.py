from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class Response(BaseModel):
    Result: str
    Code: str
    Message: str
    Data: List[dict[str, Any]]