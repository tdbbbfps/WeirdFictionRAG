import chunk
import chromadb
from google import genai
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

model = SentenceTransformer("all-MiniLM-L6-v2")

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection("fiction")

# Convert text to embedding vector array.
def embed(text : str) -> list[float]:
    embeddings = model.encode([text])
    return embeddings[0].tolist()

# Create vector database
def create_db() -> None:
    for idx, c in enumerate(chunk.get_chunks()):
        print(f"Process: {c}")
        embedding = embed(c)
        chromadb_collection.upsert(
            ids=str(idx),
            documents=c,
            embeddings=embedding
        )
# Query vector database
def query_db(question : str) -> list[str]:
    question_embedding = embed(question)
    result = chromadb_collection.query(
        query_embeddings=question_embedding,
        n_results=5 # 回傳5條最相關的內容
    )
    assert result["documents"]
    return result["documents"][0]

if __name__ == "__main__":
    # create_db()
    question = input("請輸入你的問題：")
    
    chunks = query_db(question)
    prompt = "Please answer user's question accroding to context\n"
    prompt += f"Question:{question}\n"
    prompt += f"Context:"
    for c in chunks:
        prompt += f"{c}\n"
        prompt += "-----\n"

    result = google_client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )
    print(result.candidates[0].content.parts[0].text)