from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import numpy as np

app = FastAPI()

DB = []


class Index(BaseModel):
    name: str
    dimension: int


class Vector(BaseModel):
    id: str
    values: List[float]
    metadata: Dict


@app.get("/health")
async def health_check():
    """Health check endpoint for the vector database."""
    return {"status": "healthy", "service": "endee-vector-db"}


class Upsert(BaseModel):
    vectors: List[Vector]


class Query(BaseModel):
    vector: List[float]
    top_k: int = 5
    include_metadata: bool = True


@app.post("/indexes")
def create_index(i: Index):
    return {"status": "ok"}


@app.post("/indexes/{name}/vectors")
def upsert(name: str, data: Upsert):

    for v in data.vectors:
        DB.append(v.dict())

    return {"status": "stored"}


def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


@app.post("/indexes/{name}/query")
def query(name: str, q: Query):

    scores = []

    for v in DB:
        s = cosine(q.vector, v["values"])
        scores.append((s, v))

    scores.sort(reverse=True, key=lambda x: x[0])

    matches = []

    for s, v in scores[: q.top_k]:
        matches.append({
            "score": s,
            "metadata": v["metadata"]
        })

    return {"matches": matches}