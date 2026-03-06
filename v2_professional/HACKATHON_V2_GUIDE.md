# 🏆 AI Policy Navigator Pro: Hackathon V2 (Full Stack)

This version represents a production-ready shift from Streamlit to a professional **Next.js + FastAPI + RAG** architecture. It fulfills all advanced requirements for high-end hackathon submissions.

## 🌟 Key Upgrades
- **Tech Stack**: Moved to **Next.js 14 (App Router)** and **FastAPI**.
- **UI/UX**: Premium chat interface built with **Tailwind CSS** and **Lucide Icons**.
- **Document Support**: Full support for **PDF, DOCX, and TXT** files.
- **Strict RAG Pipeline**: Ensures the AI answers **strictly** from the document.
- **API First**: Clean separation between frontend logic and AI processing.
- **Advanced Analytics**: Built-in tracking for RAG latency, language distribution, and user satisfaction.

## 📊 Analytics & System Intelligence
The V2 stack includes a professional analytics dashboard accessible at `/analytics`.
- **Query Tracking**: Monitors success rate and language trends.
- **Performance**: High-fidelity RAG latency monitoring (Retrieval vs Generation).
- **Feedback**: Integrated 👍/👎 feedback system with real-time satisfaction scoring.
- **Schema**: Production-ready PostgreSQL schema located in `analytics/schema.sql`.

## 📂 Project Structure
```text
v2_professional/
├── backend/
│   ├── main.py          # FastAPI Application & Endpoints
│   ├── processor.py     # Multi-format Text Extraction & Chunking
│   ├── rag.py           # FAISS Vector Storage & Search Logic
│   └── requirements.txt # Python Dependencies
└── frontend/
    ├── app/
    │   └── page.tsx      # Main React Chat Component
    ├── package.json      # Node.js Dependencies
    └── tailwind.config.js # Styling Configuration
```

## 🛠️ Instructions to Run

### 1. Start the Backend (API)
```bash
cd v2_professional/backend
pip install -r requirements.txt
python main.py
```
*The API will start at `http://localhost:8000`*

### 2. Start the Frontend (UI)
```bash
cd v2_professional/frontend
npm install
npm run dev
```
*The UI will start at `http://localhost:3000`*

## 🤖 Example Queries & Responses
| User Query | Document Content | Expected AI Response |
| :--- | :--- | :--- |
| "What is the age limit?" | "Eligibility: Above 60 years." | "Based on the document: Eligibility is above 60 years." |
| "What is the interest rate?" | *[Not in document]* | "The answer is not available in the uploaded document." |
| "Show highlights" | "Benefits: 1. Health 2. Money" | "Based on the document: Benefits include Health and Money." |

## 🛡️ Strict Context Policy
The `RAGSystem` in `rag.py` is configured with a strict template and a keyword threshold. If the retrieval score is low or the LLM output contains uncertainty phrases, the system defaults to the required: **"The answer is not available in the uploaded document."**
