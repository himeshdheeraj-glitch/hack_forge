-- AI Policy Navigator: Analytics Database Schema (PostgreSQL)

-- 1. Query Logs (Tracks every user interaction)
CREATE TABLE query_logs (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    response_text TEXT,
    language VARCHAR(10) DEFAULT 'en',
    latency_ms INT,
    status VARCHAR(20), -- 'success', 'no_context', 'error'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Document Metrics (Tracks processing load)
CREATE TABLE document_metrics (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    page_count INT,
    chunk_count INT,
    vector_ids JSONB, -- Array of IDs in FAISS/Chroma
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. RAG Performance (Detailed retrieval metrics)
CREATE TABLE rag_performance (
    id SERIAL PRIMARY KEY,
    query_id INT REFERENCES query_logs(id),
    retrieval_time_ms INT,
    top_chunk_id TEXT,
    relevance_score FLOAT,
    llm_generation_time_ms INT
);

-- 4. User Feedback (Satisfaction tracking)
CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    query_id INT REFERENCES query_logs(id),
    is_helpful BOOLEAN NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Scheme Popularity (Business intelligence)
CREATE TABLE scheme_analytics (
    scheme_name VARCHAR(255) PRIMARY KEY,
    recommendation_count INT DEFAULT 0,
    search_count INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
