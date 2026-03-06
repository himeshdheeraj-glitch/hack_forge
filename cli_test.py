import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from modules.pdf_processor import get_text_chunks
from modules.chatbot import PolicyChatbot

def cli_demo():
    print("--- 🏛️ AI Policy Navigator CLI Test ---")
    print("Initializing AI Engine (this may download models)...")
    
    try:
        bot = PolicyChatbot()
        
        # Sample data to index
        sample_text = """
        Govt Scheme: PM Kisan Samman Nidhi
        Objective: To provide income support to all landholding farmers' families.
        Benefit: Rs.6000/- per year in three equal installments of Rs.2000/-.
        Eligibility: All landholding farmers' families with cultivable land in their names.
        """
        
        print("Indexing sample policy data...")
        chunks = get_text_chunks(sample_text)
        metadatas = [{"source": "CLI_Sample"}] * len(chunks)
        
        bot.load_policies(chunks, metadatas)
        print("Knowledge base ready!")
        
        # Test Query
        question = "How much money do farmers get in PM Kisan?"
        print(f"\nUser: {question}")
        
        response = bot.ask(question)
        
        print(f"\nAI: {response['answer']}")
        print(f"Confidence: {response['confidence']}%")
        print(f"Sources: {[s['source'] for s in response['sources']]}")
        
        print("\n✅ CLI Test Successful! The AI backend is functional.")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    cli_demo()
