from fastapi import FastAPI, UploadFile, File
import os

# services
from services.file_processor import extract_text, chunk_text
from services.embedding_service import generate_embeddings, embed_query
from services.vector_store import store_chunks, query_chunks
from services.llm_service import generate_answer, generate_sql, clean_sql, is_safe_query
from services.router import route_query
from services.sql_service import run_sql_query
from services.logger import log_query
import time

app = FastAPI()

# directory to store uploaded files
UPLOAD_DIR = "data"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -------------------- HEALTH CHECK --------------------
@app.get("/")
def home():
    return {"message": "AI Data Copilot Running"}


# -------------------- UPLOAD + PROCESS --------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # extract text
    text = extract_text(file_path)

    # chunk text
    chunks = chunk_text(text)

    # generate embeddings
    embeddings = generate_embeddings(chunks)

    # store in vector DB
    store_chunks(chunks, embeddings)

    return {
        "filename": file.filename,
        "chunks_created": len(chunks),
        "status": "stored successfully"
    }


@app.get("/ask")
def ask(query: str):
    route = route_query(query)

    # ---------- SQL PATH ----------
    if route == "sql":
        raw_sql = generate_sql(query)
        sql_query = clean_sql(raw_sql)

        if not is_safe_query(sql_query):
            return {
                "error": "Unsafe query detected",
                "generated_sql": sql_query
            }

        try:
            result = run_sql_query(sql_query)
        except Exception as e:
            return {
                "error": str(e),
                "generated_sql": sql_query
            }

        return {
            "type": "sql",
            "question": query,
            "generated_sql": sql_query,
            "result": result,
            "explanation": {
                "rows_returned": len(result)
            }
        }

    # ---------- RAG PATH ----------
    else:
        query_embedding = embed_query(query)
        chunks = query_chunks(query_embedding)
        answer = generate_answer(chunks, query)

        return {
            "type": "rag",
            "question": query,
            "answer": answer,
            "explanation": {
                "retrieved_chunks": chunks,
                "num_chunks": len(chunks)
            }
        }

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
