from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import torch

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "google/flan-t5-small"

class RAGSystem:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = None
        self.qa_chain = None
        self._initialize_llm()

    def _initialize_llm(self):
        device = 0 if torch.cuda.is_available() else -1
        self.llm = HuggingFacePipeline.from_model_id(
            model_id=LLM_MODEL,
            task="text2text-generation",
            device=device,
            pipeline_kwargs={"max_length": 512, "temperature": 0.1}
        )

    def build_index(self, chunks, metadatas):
        self.vector_store = FAISS.from_texts(
            chunks, self.embeddings, metadatas=metadatas
        )
        self._setup_qa_chain()

    def _setup_qa_chain(self):
        template = """
        Context: {context}
        Question: {question}
        Answer based ONLY on the context. If not present, say "The answer is not available in the uploaded document."
        Answer:"""
        
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def answer(self, question):
        if not self.qa_chain:
            return "Please upload a document first.", []
        
        result = self.qa_chain.invoke({"query": question})
        answer = result["result"]
        
        # Strict context check
        if any(phrase in answer.lower() for phrase in ["don't know", "not in context", "not mentioned"]):
            return "The answer is not available in the uploaded document.", []
            
        sources = [doc.metadata.get("source") for doc in result["source_documents"]]
        return answer, list(set(sources))
