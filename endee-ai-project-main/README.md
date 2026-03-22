# Endee AI Chatbot (PDF Question Answering App)

This project is a Streamlit-based AI chatbot that can read PDF files and answer questions from the document.

The app allows you to:

- Upload PDF
- Index document text
- Ask questions
- Get answers from PDF content

This version is fully free and works on Streamlit Cloud.

No FastAPI  
No Ollama  
No paid API  
No backend server  

---

## Project Structure
endee-ai-project
│
├ streamlit_code.py
├ rag.py
├ tools.py
├ db.py
├ pdf_loader.py
├ requirements.txt
├ README.md

---

## Features

- PDF text extraction
- Text chunking
- Embedding search using Sentence Transformers
- Question answering from document
- Streamlit UI
- Deployable on Streamlit Cloud

---

## Requirements

Python 3.9+

Install dependencies:

```
pip install -r requirements.txt
```

requirements.txt:

```
streamlit
pypdf
sentence-transformers
numpy
torch
```

---

## Run Locally

Run this command:

```
streamlit run streamlit_code.py
```

Open browser:

```
http://localhost:8501
```

---

## How it Works

1. Upload PDF
2. PDF text extracted
3. Text split into chunks
4. Embeddings created
5. Question embedding created
6. Best matching text returned

No external API used.

---

## Deployment on Streamlit Cloud

Steps:

1. Push project to GitHub
2. Go to Streamlit Cloud
3. Click New App
4. Select repository
5. Select branch = main
6. Main file =

```
streamlit_code.py
```

7. Click Deploy

App will run online.

---

## GitHub Push Commands

```
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

---

## Troubleshooting

### Module error

```
pip install -r requirements.txt
```

### Streamlit not found

```
pip install streamlit
```

### PDF not reading

Check file type = pdf

### Deployment error

Check main file:

```
streamlit_code.py
```

---

## Technologies Used

- Python
- Streamlit
- Sentence Transformers
- PyPDF
- NumPy
- Torch

---

## Author

Pooja Gupta

AI / ML Student Project

```

---

# ✅ How to add README

In terminal:

```
notepad README.md
```

Paste text → save

Then:

```
git add README.md
git commit -m "added readme"
git push
```

---

If you want, I can also give **professional README with badges + images + demo section**.
