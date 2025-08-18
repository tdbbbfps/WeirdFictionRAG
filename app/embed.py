import chunk
import chromadb
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
google_client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-exp-03-07"
LLM_MODEL = "gemini-2.5-flash-lite"

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection("fiction")
def embed(text : str, is_store : bool) -> list[float]:
    result = google_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={
            "task_type": "RETRIEVAL_DOCUMENT" if (is_store) else "RETRIEVAL_QUERY" # Google Embedding模型接口有查詢與儲存
        }
    )
    assert result.embeddings
    assert result.embeddings[0].values # 為了方便直接用assert 實務上要做錯誤處理
    return result.embeddings[0].values

def create_db() -> None:
    for idx, c in enumerate(chunk.get_chunks()):
        print(f"Process: {c}")
        embedding = embed(c, True)
        chromadb_collection.upsert(
            ids=str(idx),
            documents=c,
            embeddings=embedding
        )
if __name__ == "__main__":
    create_db()