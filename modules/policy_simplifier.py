def simplify_policy_text(legal_text, llm):
    """
    Converts complex legal language into simple human-readable text.
    """
    prompt = f"""
    Simplification Task:
    Convert the following complex government policy text into simple, easy-to-understand language that a common citizen can understand. 
    Focus on what it means for them.

    Complex Text:
    {legal_text}

    Simplified Version:"""
    
    response = llm.invoke(prompt)
    return response

def summarize_policy(vector_store, llm, full_text=""):
    """
    Uses RAG to extract all important points from the policy without duplicates.
    Includes a fallback for Lite Mode.
    """
    context = ""
    
    # 1. Try RAG Retrieval (Top 20 chunks for depth)
    if vector_store and llm:
        try:
            query = "What are the most important points, benefits, eligibility criteria, and critical information in this policy? List everything significant without duplicates."
            docs = vector_store.similarity_search(query, k=20)
            context = "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Summarization retrieval error: {e}")

    # 2. Fallback to Full Text if RAG fails or context is too small
    if (not context or len(context) < 500) and full_text:
        # Use first 8000 chars of full text as a heuristic fallback
        context = full_text[:8000]

    if not context:
        return "No sufficient policy data found to generate insights."

    # 3. LLM Synthesis
    if llm:
        prompt = f"""
        Policy Insight Task:
        Based on the following excerpts from a government policy document, extract ALL unique important points.
        
        Requirements:
        1. Capture all Benefits, Eligibility rules, and critical Deadlines/Steps.
        2. Ensure there are NO duplicate or redundant points.
        3. Even if the text is a list of questions, extract the core policy facts.
        4. Use simple, direct, white-colored (formatted) bullet points.

        Policy Context:
        {context}

        Important Facts & Insights:"""
        
        try:
            response = llm.invoke(prompt)
            return response
        except Exception as e:
            return f"Error generating brain insights: {str(e)}"
    
    return "AI Model not ready for deep summarization. Please check the Highlights Card below."
