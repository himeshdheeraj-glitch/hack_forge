import os
import torch
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configure local model paths or names
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-small" 

class RAGPipeline:
    def __init__(self, lazy=True):
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        self.llm = None
        self.model_status = "Not Loaded"
        self.lite_mode = True # Default to lite mode for speed
        self.indexed_text = "" # Store plain text for lite search

    def initialize_models(self):
        """Initializes both embedding and LLM models for Neural RAG."""
        if self.model_status == "Ready":
            return
            
        self.model_status = "Loading AI Models..."
        try:
            # 1. Initialize Embeddings
            if self.embeddings is None:
                self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            
            # 2. Initialize LLM
            if self.llm is None:
                self._setup_llm()
                
            self.model_status = "Ready"
            self.lite_mode = False
        except Exception as e:
            self.model_status = f"Error: {str(e)}"
            # Fallback to lite mode on error
            self.lite_mode = True
            print(f"RAG init error: {e}")

    def _setup_llm(self):
        """Initializes the local LLM using HuggingFace."""
        device = 0 if torch.cuda.is_available() else -1
        try:
            self.llm = HuggingFacePipeline.from_model_id(
                model_id=LLM_MODEL,
                task="text2text-generation",
                device=device,
                pipeline_kwargs={
                    "max_length": 512,
                    "temperature": 0.1,
                    "top_p": 0.95,
                    "repetition_penalty": 1.15
                }
            )
        except Exception as e:
            print(f"LLM setup error: {e}")
            raise e

    def build_vector_store(self, chunks, metadatas, text_content=""):
        """Creates the vector store and also stores chunks for Lite Mode."""
        self.indexed_text = text_content
        self.chunks = chunks # Store chunks for Lite Search
        self.metadatas = metadatas
        
        if not chunks:
            return None
        
        if self.model_status == "Ready":
            try:
                self.vector_store = FAISS.from_texts(
                    texts=chunks,
                    embedding=self.embeddings,
                    metadatas=metadatas
                )
                self._setup_qa_chain()
            except Exception as e:
                print(f"FAISS Build Error: {e}")
        
        return True

    def _setup_qa_chain(self):
        """Sets up the RetrievalQA chain."""
        if not self.vector_store or not self.llm:
            return

        template = """
        Context: {context}
        Question: {question}
        
        Answer this question in clear, complete sentences based ONLY on the context provided. 
        Do not use bullet points or lists unless specifically asked.
        If the context does not contain the answer, say: "The uploaded document does not contain information about this question."
        
        Answer:"""
        
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 4}), 
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def answer_question(self, question):
        """Answers a question using Neural RAG or Refined Sentence Extraction."""
        # 1. Try Neural RAG if ready
        if self.qa_chain and self.model_status == "Ready":
            try:
                result = self.qa_chain.invoke({"query": question})
                ans = result["result"].strip()
                
                # Validation against hallucinatory fragments
                if len(ans) < 5 or "information about this question" in ans.lower():
                    return "The uploaded document does not contain information about this question.", []
                
                # Ensure it's a full sentence (basic check)
                if not ans.endswith('.') and not ans.endswith('?') and not ans.endswith('!'):
                    ans += "."
                    
                return ans, [{"source": d.metadata.get("source", "Doc"), "content": d.page_content} for d in result["source_documents"]]
            except Exception as e:
                print(f"RAG Error: {e}")

        # 2. Refined Lite Fallback (Sentence-focused Extraction)
        q_words = [w.lower() for w in question.split() if len(w) > 3]
        if not q_words: q_words = [w.lower() for w in question.split()]
        
        scored_chunks = []
        for i, chunk in enumerate(getattr(self, 'chunks', [])):
            chunk_l = chunk.lower()
            score = sum(1 for word in q_words if word in chunk_l)
            if score > 0:
                scored_chunks.append((score, i, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        if scored_chunks and scored_chunks[0][0] >= 1:
            best_chunk = scored_chunks[0][2]
            # Try to find the most relevant sentence within the chunk
            sentences = [s.strip() for s in best_chunk.split('.') if len(s.strip()) > 10]
            best_sentence = sentences[0] if sentences else best_chunk
            
            for s in sentences:
                if any(w in s.lower() for w in q_words):
                    best_sentence = s
                    break
            
            # Formulate as a professional sentence
            ans = f"According to the document, {best_sentence}."
            if not ans.endswith('.'): ans += "."
            
            sources = [{"source": self.metadatas[scored_chunks[0][1]].get("source", "Policy Doc"), "content": best_chunk}]
            return ans, sources
        
        return "The uploaded document does not contain information about this question.", []
