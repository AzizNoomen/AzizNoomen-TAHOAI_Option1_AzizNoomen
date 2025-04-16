from pydantic import BaseModel
from typing import Optional


class GenericResponse(BaseModel):
    response: Optional[str] = None

class OllamaResponse(BaseModel):
    label: str
    confidence: float
