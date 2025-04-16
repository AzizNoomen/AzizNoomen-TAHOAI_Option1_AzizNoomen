from pydantic import BaseModel
from typing import Any, Dict, Optional, List

class OllamaModelDetails(BaseModel):
    parent_model: str
    format: str
    family: str
    families: List[str]
    parameter_size: str
    quantization_level: str

class OllamaModel(BaseModel):
    name: str
    model: str
    modified_at: str
    size: int
    digest: str
    details: OllamaModelDetails

class OllamaModelListResponse(BaseModel):
    response: List[OllamaModel]

class ShowModelResponse(BaseModel):
    license: str
    modelfile: str
    parameters: str
    template: str
    details: OllamaModelDetails

class ShowModelFullResponse(BaseModel):
    response: ShowModelResponse

class GenericResponse(BaseModel):
    response: Optional[str] = None

class OllamaRequest(BaseModel):
    text: str

class OllamaResponse(BaseModel):
    label: str
    confidence: float
