from modules.recommender import get_recommendations

def test_recommender():
    print("--- 📋 Policy Recommendation Engine Test ---")
    
    test_profiles = [
        {
            'name': 'Small Farmer',
            'data': {'age': 45, 'income': 200000, 'occupation': 'Farmer', 'is_farmer': True, 'state': 'Telangana'}
        },
        {
            'name': 'Senior Citizen',
            'data': {'age': 65, 'income': 400000, 'occupation': 'Retired', 'is_farmer': False, 'state': 'Delhi'}
        }
    ]
    
    for profile in test_profiles:
        print(f"\nProfile: {profile['name']}")
        print(f"Data: {profile['data']}")
        recs = get_recommendations(profile['data'])
        print("Recommended Schemes:")
        for r in recs:
            print(f"- {r['name']}: {r['benefit'][:60]}...")

if __name__ == "__main__":
    test_recommender()
