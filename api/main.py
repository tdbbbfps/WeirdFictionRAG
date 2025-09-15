from fastapi import FastAPI
import ollama
from pydantic import BaseModel


# Define request model's property
class RequestModel(BaseModel):
    prompt : str
    model : str

# uvicorn main:app --reload
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/hello")
async def msg(name: str):
    return {"message": f"Hello {name}"}

@app.post("/generate")
async def generate(data : RequestModel):
    response = ollama.chat(model=data.model, messages=[{"role": "user", "content": data.prompt}])
    return {"response": response['message']['content']}

# Get ollama local models' name.
@app.get("/models")
async def get_ollama_models():
    models_info = ollama.list()
    models = []
    for model in models_info["models"]:
        models.append(model.model)
    return models

