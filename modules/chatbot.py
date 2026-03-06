from modules.rag_pipeline import RAGPipeline

class PolicyChatbot:
    def __init__(self):
        self.rag = RAGPipeline()
        self.history = []

    def load_policies(self, chunks, metadatas):
        """Initializes the RAG system with policy data."""
        if not chunks:
            return False
        self.rag.build_vector_store(chunks, metadatas)
        return True

    def ask(self, question):
        """Process a user question and returns structured response."""
        answer, sources = self.rag.answer_question(question)
        
        # Calculate a mock confidence score based on retrieval success and LLM output length
        # In a real system, you'd get this from the model's logprobs or a dedicated scoring model
        confidence = 0.0
        if answer and "don't know" not in answer.lower():
            if len(sources) > 0:
                confidence = 0.85 + (min(len(answer), 500) / 1000) * 0.1
            else:
                confidence = 0.4 # Hallucination risk or general knowledge answer
        
        # Clip confidence
        confidence = min(max(confidence, 0.0), 1.0)
        
        response = {
            "answer": answer,
            "sources": sources,
            "confidence": round(confidence * 100, 2)
        }
        
        self.history.append({"question": question, "answer": response})
        return response

    def get_history(self):
        return self.history
