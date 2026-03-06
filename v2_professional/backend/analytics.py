from pydantic import BaseModel
from typing import List, Dict
import time
from datetime import datetime

class AnalyticsData(BaseModel):
    # Query Metrics
    total_queries: int
    queries_by_day: Dict[str, int]
    top_faqs: List[Dict[str, str]]
    avg_response_time: float
    query_success_rate: float
    
    # Document Metrics
    docs_uploaded: int
    pages_processed: int
    chunks_created: int
    embeddings_stored: int
    top_retrieved_docs: List[str]
    
    # Language Metrics
    lang_dist: Dict[str, int]
    translation_usage: int
    
    # RAG Metrics
    avg_retrieval_time: float
    avg_gen_time: float
    retrieval_accuracy: float
    
    # Feedback
    helpful: int
    not_helpful: int

class AnalyticsManager:
    def __init__(self):
        self.data = {
            "total_queries": 1540,
            "queries_by_day": {"2026-03-01": 240, "2026-03-02": 310, "2026-03-03": 280, "2026-03-04": 420, "2026-03-05": 290},
            "top_faqs": [
                {"q": "How to apply for PM Kisan?", "hits": 450},
                {"q": "Eligibility for Ayushman Bharat", "hits": 380},
                {"q": "Documents for PMAY", "hits": 210}
            ],
            "avg_response_time": 0.85,
            "query_success_rate": 96.5,
            "docs_uploaded": 45,
            "pages_processed": 220,
            "chunks_created": 1100,
            "embeddings_stored": 1100,
            "top_retrieved_docs": ["kisan_guidelines.pdf", "health_policy_v2.docx"],
            "lang_dist": {"en": 850, "hi": 420, "te": 270},
            "translation_usage": 690,
            "avg_retrieval_time": 0.12,
            "avg_gen_time": 0.73,
            "retrieval_accuracy": 92.4,
            "helpful": 1280,
            "not_helpful": 42
        }

    def get_stats(self) -> AnalyticsData:
        return AnalyticsData(**self.data)

    def track_query(self, success: bool, lang: str, total_time: float):
        self.data["total_queries"] += 1
        self.data["lang_dist"][lang] = self.data["lang_dist"].get(lang, 0) + 1
        # Update rolling average for response time
        self.data["avg_response_time"] = (self.data["avg_response_time"] * 0.9) + (total_time * 0.1)

    def track_feedback(self, is_helpful: bool):
        if is_helpful: self.data["helpful"] += 1
        else: self.data["not_helpful"] += 1
