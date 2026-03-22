import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pdf_loader import load_pdf
from db import store_documents
from tools import vector_search_tool
from rag import generate_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"status": "healthy", "service": "ai-document-qa-api"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        # Save to a temp file so pypdf can read it
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        docs = load_pdf(tmp_path)
        os.unlink(tmp_path)

        if not docs:
            return {"error": "No text could be extracted from the PDF"}

        success = store_documents(docs)
        if success:
            return {"status": f"PDF indexed successfully ({len(docs)} chunks)"}
        else:
            return {"error": "Failed to store documents in vector database"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/ask")
def ask(q: Question):
    try:
        docs = vector_search_tool(q.question)
        if not docs:
            return {"error": "No relevant documents found. Please upload a PDF first."}
        answer = generate_answer(q.question, docs)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
