from sentence_transformers import SentenceTransformer
from endee_client import create_index, upsert

model = SentenceTransformer("all-MiniLM-L6-v2")


def store_documents(docs):
    """Store document chunks in the vector database"""
    try:
        # Create index if it doesn't exist
        if not create_index():
            print("Failed to create index")
            return False

        stored_count = 0
        for doc in docs:
            text = doc.get("text", "")
            if text:
                # Generate embedding for the text chunk
                emb = model.encode(text).tolist()
                # Store in Endee
                if upsert(text, emb):
                    stored_count += 1
                else:
                    print(f"Failed to store document chunk")

        print(f"Successfully stored {stored_count}/{len(docs)} documents")
        return stored_count > 0
    except Exception as e:
        print(f"Error storing documents: {e}")
        return False