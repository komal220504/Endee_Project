import os
import requests
import uuid

# Endee vector database server should usually run on 8000 when FastAPI app is on 8001
ENDEE_URL = os.getenv("ENDEE_URL", "http://127.0.0.1:8000")
INDEX_NAME = "docs"
DIM = 384


def create_index():
    try:
        response = requests.post(
            f"{ENDEE_URL}/indexes",
            json={"name": INDEX_NAME, "dimension": DIM},
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error creating index: {e}")
        return False


def upsert(text, embedding):
    try:
        vec = {
            "id": str(uuid.uuid4()),
            "values": embedding,
            "metadata": {"text": text}
        }

        response = requests.post(
            f"{ENDEE_URL}/indexes/{INDEX_NAME}/vectors",
            json={"vectors": [vec]},
            timeout=5
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error upserting vector: {e}")
        return False


def query_endee(embedding):

    def _do_query(base_url):
        return requests.post(
            f"{base_url}/indexes/{INDEX_NAME}/query",
            json={
                "vector": embedding,
                "top_k": 3,
                "include_metadata": True
            },
            timeout=10,
        )

    # try configured endpoint first
    endpoints = [ENDEE_URL]

    # fallback 8000/8001 if user has wrong default
    if ENDEE_URL.endswith(":8000"):
        endpoints.append("http://127.0.0.1:8001")
    elif ENDEE_URL.endswith(":8001"):
        endpoints.append("http://127.0.0.1:8000")

    last_error = None

    for endpoint in endpoints:
        try:
            r = _do_query(endpoint)
        except Exception as exc:
            last_error = exc
            continue

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError as e:
                # repair malformed JSON that may have an accidental status prefix
                text = r.text.strip()
                if text.startswith("200 "):
                    text = text[4:].strip()
                try:
                    import json
                    return json.loads(text)
                except Exception:
                    raise ValueError(f"Extra data parsing Endee JSON: {e} - body: {r.text}")

        # if this endpoint is invalid, try fallback URL
        last_error = ValueError(f"{endpoint} -> HTTP {r.status_code}: {r.text}")

        if r.status_code in (404, 405):
            continue
        else:
            break

    if last_error is not None:
        raise last_error

    raise ValueError("Unable to query Endee; no endpoint succeeded.")
