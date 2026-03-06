def get_recommendations(user_data):
    """
    Recommends schemes based on user profile data.
    user_data example: {
        'age': 65,
        'income': 400000,
        'occupation': 'Farmer',
        'is_farmer': True,
        'state': 'Telangana',
        'district': 'Hyderabad'
    }
    """
    recommendations = []
    
    # 1. Healthcare
    if user_data.get('income', 0) < 500000:
        recommendations.append({
            "name": "Ayushman Bharat (PM-JAY)",
            "benefit": "Health coverage up to ₹5 lakh per family per year for secondary and tertiary care hospitalization.",
            "category": "Healthcare"
        })
    
    # 2. Agriculture
    if user_data.get('is_farmer'):
        recommendations.append({
            "name": "PM Kisan Samman Nidhi",
            "benefit": "Income support of ₹6,000 per year in three equal installments directly to bank accounts of small/marginal farmers.",
            "category": "Agriculture"
        })
        
        if user_data.get('state') == 'Telangana':
            recommendations.append({
                "name": "Rythu Bandhu (Telangana)",
                "benefit": "Investment support to farmers for two crops a year.",
                "category": "Agriculture"
            })

    # 3. Social Security / Pension
    if user_data.get('age', 0) >= 60:
        recommendations.append({
            "name": "Pradhan Mantri Vaya Vandana Yojana (PMVVY)",
            "benefit": "Pension scheme for senior citizens aged 60 and above with guaranteed returns.",
            "category": "Social Security"
        })
        
    # 4. Housing
    if user_data.get('income', 0) < 600000:
        recommendations.append({
            "name": "Pradhan Mantri Awas Yojana (PMAY)",
            "benefit": "Affordable housing for urban and rural poor with interest subsidies on home loans.",
            "category": "Housing"
        })

    # 5. State Specific (Examples)
    if user_data.get('state') == 'Telangana':
        recommendations.append({
            "name": "Kalyana Lakshmi / Shaadi Mubarak",
            "benefit": "Financial assistance for the marriage of girls from poor families.",
            "category": "Social Welfare"
        })

    return recommendations
