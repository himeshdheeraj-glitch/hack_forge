from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
import time
from .processor import DocumentProcessor
from .rag import RAGSystem
from .analytics import AnalyticsManager

app = FastAPI()
analytics = AnalyticsManager()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

processor = DocumentProcessor()
rag = RAGSystem()

class ChatRequest(BaseModel):
    message: str

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        text = processor.extract_text(file_path)
        chunks, metas = processor.create_chunks(text, file.filename)
        rag.build_index(chunks, metas)
        
        return {"message": f"Successfully indexed {file.filename}", "chunks": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        start_time = time.time()
        answer, sources = rag.answer(request.message)
        latency = time.time() - start_time
        analytics.track_query(success=True, lang="en", total_time=latency)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        analytics.track_query(success=False, lang="en", total_time=0)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics")
async def get_analytics():
    return analytics.get_stats()

@app.post("/feedback")
async def feedback(helpful: bool):
    analytics.track_feedback(helpful)
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
