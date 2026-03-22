from pypdf import PdfReader


def chunk_text(text, size=500):

    chunks = []

    for i in range(0, len(text), size):
        chunks.append(text[i:i+size])

    return chunks


def load_pdf(path):

    reader = PdfReader(path)

    docs = []

    for page in reader.pages:

        text = page.extract_text()

        if not text:
            continue

        parts = chunk_text(text)

        for p in parts:
            docs.append({"text": p})

    return docs