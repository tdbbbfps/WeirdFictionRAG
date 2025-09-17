from fastapi import APIRouter
from schemas import RequestModel
import ai.embed

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Here's api router."}

@router.get("get-system-prompt")
async def get_system_prompt():
    return {"system_prompt": ""}

@router.put("/update-system-prompt")
async def update_system_prompt(system_prompt: str):
    pass

# Get user's ollama local models.
@router.get("/models")
async def get_ollama_models():
    models_info = ollama.list()
    models = []
    for model in models_info["models"]:
        models.append(model.model)
    return {"model": models}