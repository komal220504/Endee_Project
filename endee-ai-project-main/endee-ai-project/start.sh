#!/bin/bash
# Endee AI - Start all services

source .venv/bin/activate

echo "Starting Endee vector DB on port 8000..."
uvicorn endee_server:app --port 8000 &
ENDEE_PID=$!

sleep 1

echo "Starting FastAPI backend on port 8001..."
uvicorn main:app --reload --port 8001 &
API_PID=$!

sleep 1

echo "Starting Streamlit UI on port 8501..."
streamlit run streamlit_code.py --server.port 8501

# Cleanup on exit
kill $API_PID $ENDEE_PID 2>/dev/null
