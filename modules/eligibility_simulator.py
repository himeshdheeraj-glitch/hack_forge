def simulate_eligibility(current_params, new_params, recommendation_engine):
    """
    Compares eligibility between current and hypothetical parameters.
    """
    current_recs = recommendation_engine(current_params)
    simulated_recs = recommendation_engine(new_params)
    
    current_names = [r['name'] for r in current_recs]
    simulated_names = [r['name'] for r in simulated_recs]
    
    gained = [n for n in simulated_names if n not in current_names]
    lost = [n for n in current_names if n not in simulated_names]
    
    return {
        "current_count": len(current_recs),
        "simulated_count": len(simulated_recs),
        "gained": gained,
        "lost": lost,
        "status": "Change Detected" if gained or lost else "No Change"
    }
