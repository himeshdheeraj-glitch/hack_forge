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
