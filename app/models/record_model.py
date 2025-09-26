from typing import Optional
from pydantic import BaseModel

class Record(BaseModel):
    """This Model is used to define the record model"""
    text: str
    rating: Optional[float] = None
    timestamp: Optional[str] = None
