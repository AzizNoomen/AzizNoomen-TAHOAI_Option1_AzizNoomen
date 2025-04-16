from fastapi import APIRouter, Body, Depends, status, Query
from dependency_injector.wiring import Provide, inject
from configuration.injection_container import DependencyContainer
from app.schemas.ollama_schemas import OllamaRequest, OllamaResponse, GenericResponse
from app.services.ollama_service import OllamaService
from app.exceptions.api_exception_handler import APIRequestException

router = APIRouter(prefix="/service")

@router.post("/answer", response_model=OllamaResponse)
@inject
async def generate_response(
                request_body: OllamaRequest = Body(...),
                ollama_service: OllamaService = Depends(Provide[DependencyContainer.ollama_service])):
    try:
        response = ollama_service.classify_document(**request_body.dict())
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

