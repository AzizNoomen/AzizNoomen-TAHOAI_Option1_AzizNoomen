from fastapi import APIRouter, Body, Depends, status, Query
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer
from app.schemas.ollama_schemas import OllamaResponse, GenericResponse
from app.services.ollama_service import OllamaService
from app.exceptions.api_exception_handler import APIRequestException

router = APIRouter()

@router.post("/classify", response_model=OllamaResponse)
@inject
def classify_text(
                text: str = Query(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])):
    try:
        response = ollama_service.classify_document(text)
        return response
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))


@router.post("/pull-model", response_model=GenericResponse)
@inject
def pull_model(model: str = Query(...),
                insecure: bool = Query(False),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])
                ):
    try:
        response = ollama_service.pull_model(model, insecure)
        return {"response": response}
    
    except ValueError as value_error:
        raise APIRequestException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(value_error))

