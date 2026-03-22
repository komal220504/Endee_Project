import streamlit as st
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
BACKEND_URL = "http://127.0.0.1:8001"
MAX_RETRIES = 3
RETRY_DELAY = 1

# Create a session with retry strategy
def create_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """Create a requests session with automatic retries."""
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# Check backend connection
def check_backend_connection():
    """Check if backend is available."""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Page config
st.set_page_config(page_title="Endee AI Chatbot", layout="wide")
st.title("Endee AI Chatbot")

# Check backend status
if not check_backend_connection():
    st.error(
        "❌ **Backend Server Not Running**\n\n"
        "The FastAPI backend is not available. Please ensure:\n"
        "1. The backend server is running on port 8001\n"
        "2. You can start it by running:"
        "\n\n```powershell\nuvicorn main:app --reload --port 8001\n```"
        "\n\nOr use the startup script: `start.bat` or `start.sh`"
    )
    st.stop()

# PDF Upload Section
st.header("📄 Upload PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if st.button("Upload and Index PDF"):
        with st.spinner("Uploading and indexing PDF... (this may take a few minutes)"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                session = create_retry_session()
                response = session.post(
                    f"{BACKEND_URL}/upload-pdf",
                    files=files,
                    timeout=120  # Increased to 2 minutes for large PDFs
                )

                if response.status_code == 200:
                    result = response.json()
                    if "status" in result:
                        st.success(f"✅ {result['status']}")
                    else:
                        st.error(result.get("error", "Unknown error"))
                else:
                    st.error(f"❌ Upload failed: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection error: Backend server is not available")
            except requests.exceptions.Timeout:
                st.error("❌ Upload timed out. Please try again.")
            except Exception as e:
                st.error(f"❌ Error uploading file: {str(e)}")

# Question Answering Section
st.header("❓ Ask Questions")
q = st.text_input("Enter your question", placeholder="What would you like to know?")

if q:
    with st.spinner("Generating answer... (this may take 30-60 seconds)"):
        try:
            session = create_retry_session()
            r = session.post(
                f"{BACKEND_URL}/ask",
                json={"question": q},
                timeout=120  # Increased to 2 minutes for LLM processing
            )

            if r.status_code == 200:
                result = r.json()
                if "answer" in result:
                    st.write("**Answer:**")
                    st.write(result["answer"])
                else:
                    st.error(result.get("error", "Unknown error"))
            else:
                st.error(f"❌ Request failed: {r.status_code}")

            # Debug info
            with st.expander("🔍 Debug Info"):
                st.write(f"Status Code: {r.status_code}")
                st.write(f"Response: {r.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Connection error: Backend server is not available")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Error processing request: {str(e)}")