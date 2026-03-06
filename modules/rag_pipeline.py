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
        """Sets up the RetrievalQA chain with a more flexible, comprehensive prompt."""
        if not self.vector_store or not self.llm:
            return

        template = """
        Document Context:
        {context}
        
        User Instruction/Question:
        {question}
        
        Role: You are an expert Policy Analyst.
        Task: Provide a detailed and accurate response based ONLY on the provided document context. 
        
        Guidelines:
        1. If it's a specific question, answer it directly.
        2. If asked to summarize, list points, or explain, do so clearly.
        3. If the answer is found in the text, provide it comprehensively.
        4. If the provided context absolutely does not contain the information, politely state that it's not in the document.
        
        Comprehensive Answer:"""
        
        QA_CHAIN_PROMPT = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            # Increased k to 6 for broader context awareness
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 6}), 
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def answer_question(self, question):
        """Answers any type of question using Neural RAG or Deep Semantic Fallback."""
        # 1. Try Neural RAG if ready
        if self.qa_chain and self.model_status == "Ready":
            try:
                result = self.qa_chain.invoke({"query": question})
                ans = result["result"].strip()
                
                # Check for "not in document" signals from the model
                not_found_signals = ["not contain information", "not found in the document", "context does not provide"]
                is_not_found = any(s in ans.lower() for s in not_found_signals)
                
                if not is_not_found and len(ans) > 10:
                    return ans, [{"source": d.metadata.get("source", "Doc"), "content": d.page_content} for d in result["source_documents"]]
            except Exception as e:
                print(f"RAG Error: {e}")

        # 2. Enhanced Lite Fallback (Broad Semantic Matching)
        # We look for ANY overlap and return a synthesis of the best parts
        q_words = [w.lower() for w in question.split() if len(w) > 3]
        if not q_words: q_words = [w.lower() for w in question.split()]
        
        scored_chunks = []
        for i, chunk in enumerate(getattr(self, 'chunks', [])):
            chunk_l = chunk.lower()
            # Score based on word frequency and proximity
            score = sum(3 if word in chunk_l else 0 for word in q_words)
            if score > 0:
                scored_chunks.append((score, i, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        if scored_chunks:
            # We take the top 2 most relevant chunks to provide a broader answer
            best_parts = []
            sources = []
            for score, idx, content in scored_chunks[:2]:
                # Extract relevant sentences
                sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 15]
                for s in sentences:
                    if any(w in s.lower() for w in q_words):
                        if s not in best_parts: best_parts.append(s)
                
                sources.append({"source": self.metadatas[idx].get("source", "Policy Doc"), "content": content})

            if best_parts:
                ans = "Based on the document highlights: " + " ".join(best_parts)
                if not ans.endswith('.'): ans += "."
                return ans, sources
        
        return "The provided document does not seem to contain specific information regarding this query.", []
