from fastapi import FastAPI
import ollama
# uvicorn main:app --reload
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

# 問號後面接參數跟值，fastapi會自動解析並對應到函數中的參數。
# http://127.0.0.1:8000/hello?name=YourName
@app.get("/hello")
async def msg(name: str):
    return {"message": f"Hello {name}"}

@app.post("/generate")
async def generate(prompt: str):
    response = ollama.chat(model="huihui_ai/deepseek-r1-abliterated", messages=[{"role": "user", "content": prompt}])
    return {"response": response['message']['content']}