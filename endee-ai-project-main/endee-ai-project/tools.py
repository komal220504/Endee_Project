from sentence_transformers import SentenceTransformer
from endee_client import query_endee

model = SentenceTransformer("all-MiniLM-L6-v2")


def vector_search_tool(query):

    emb = model.encode(query).tolist()

    res = query_endee(emb)

    matches = res.get("matches", [])

    docs = []

    for m in matches:
        docs.append(m["metadata"]["text"])

    return docs