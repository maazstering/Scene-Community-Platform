from pydantic import BaseModel
from typing import Optional


class CircleCreate(BaseModel):
    name: str
    description: Optional[str] = None