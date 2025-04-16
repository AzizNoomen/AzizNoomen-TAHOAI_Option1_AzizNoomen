import requests
import json
from fastapi import HTTPException
from typing import Generator
from configuration.config import app_config
from app.schemas.ollama_schemas import OllamaResponse
from app.exceptions.service_exceptions import ModelNotFoundException
from configuration.logging import logger

class OllamaService:

    def generate_text(self, model: str, prompt: str, system: str = None, template: str = None, context: str = None, options: str = None) -> Generator[str, None, None]:
        
        try:
            url = f"{app_config.BASE_URL}/api/generate"
            payload = {
                "model": model,
                "prompt": prompt,
                "system": system,
                "template": template,
                "context": context,
                "options": options
                }
            
            payload = {k: v for k, v in payload.items() if v is not None}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if not chunk.get("done"):
                            response_piece = chunk.get("response", "")
                            yield response_piece
                            full_response += response_piece
                return full_response

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        


    def pull_model(self, model: str, insecure: bool = False) -> str:
        
        try:
            url = f"{app_config.BASE_URL}/api/pull"
            payload = {"name": model, "insecure": insecure}

            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'Completed' in chunk:
                            logger.info(f" - Completed: {chunk['Completed']}")
                            return f"Model '{model}' pulled successfully"
                        
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        

    def check_ollama_health(self) -> str:
        try:
            url = f"{app_config.BASE_URL}/"
            response = requests.head(url)
            response.raise_for_status()
            return "Ollama is running"
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
  

    def classify_document(self, text: str, model:str="mistral:latest") -> dict:
        prompt = (
            f"Classify the following document text into one of the following types: "
            f"invoice, resume, or contract.\n\n"
            f"Return the result ONLY as a JSON object with this exact format and nothing else:\n"
            f'{{\n  "label": "DocumentType",\n  "confidence": score\n}}\n\n'
            f"Text:\n{text}")

        response_generator = self.generate_text(model, prompt=prompt)
        
        # Collect the response pieces (it could come in chunks)
        full_response = ""
        for response_piece in response_generator:
            full_response += response_piece
        logger.info("full response", full_response)
        
        try:
            result = json.loads(full_response)

            if "label" in result and "confidence" in result:
                return OllamaResponse(label=result["label"], confidence=result["confidence"])
            else:
                raise ValueError("Invalid response format")

        except (json.JSONDecodeError, ValueError) as e:
            return OllamaResponse(label="Unknown", confidence=0.0)

