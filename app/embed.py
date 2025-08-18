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

# 將文字轉換為向量陣列
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
# 創建向量資料庫
def create_db() -> None:
    for idx, c in enumerate(chunk.get_chunks()):
        print(f"Process: {c}")
        embedding = embed(c, True)
        chromadb_collection.upsert(
            ids=str(idx),
            documents=c,
            embeddings=embedding
        )
# 查詢向量資料庫
def query_db(question : str) -> list[str]:
    question_embedding = embed(question, False)
    result = chromadb_collection.query(
        query_embeddings=question_embedding,
        n_results=5 # 回傳5條最相關的內容
    )
    assert result["documents"]
    return result["documents"][0]

if __name__ == "__main__":
    question = input("請輸入你的問題：")
    # create_db()
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
    print(result)