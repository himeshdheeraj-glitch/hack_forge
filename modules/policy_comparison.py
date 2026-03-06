def compare_schemes(scheme_a_text, scheme_b_text, llm):
    """
    Uses the LLM to compare two scheme texts and return a structured comparison.
    """
    prompt = f"""
    Comparison Task:
    Compare the following two government schemes based on:
    1. Benefit Amount
    2. Eligibility Criteria
    3. Application Method
    4. Target Group

    Scheme A:
    {scheme_a_text}

    Scheme B:
    {scheme_b_text}

    Provide the comparison in a concise, point-wise format.
    """
    
    # We use the llm instance from rag_pipeline
    response = llm.invoke(prompt)
    return response

def get_comparison_table(comparison_text):
    """
    Parses comparison text into a dictionary for a table (simplified mockup).
    In a real app, you'd use structured output (JSON).
    """
    # Simple mockup for hackathon UI
    return {
        "Feature": ["Benefit", "Eligibility", "Application"],
        "Scheme A": ["Up to ₹5 Lakh", "Income < ₹5L", "Online/CSC"],
        "Scheme B": ["₹6,000/year", "Landowner Farmer", "DBT"]
    }
