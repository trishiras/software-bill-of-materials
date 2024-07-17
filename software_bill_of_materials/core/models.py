from datetime import datetime
from pydantic import Field, BaseModel
from typing import Optional, List, Any, Dict


class Response(BaseModel):
    """
    Represents the response structure.
    """

    data: List[str] = Field(default_factory=list)
    success: bool = Field(default=False)
    message: Optional[str] = Field(default=None)
    status_code: int = Field(default=200)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    meta: Dict[str, Any] = Field(default_factory=dict)
