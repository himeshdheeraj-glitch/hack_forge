import re
from urllib.parse import urlparse

def detect_fraud(text, vector_store=None):
    """
    Advanced fraud detection analyzing document content for suspicious indicators.
    Returns: (Level, Status, Formatted Report, Risk Percentage)
    """
    # 1. Basic Entity Extraction
    scheme_name = "Not detected clearly"
    name_patterns = [
        r"(?:Scheme|Mission|Yojana|Policy|Program|Programme):\s*([^\n,.]+)",
        r"^([^ \n]+ (?:Yojana|Scheme|Mission|Policy))",
    ]
    for p in name_patterns:
        match = re.search(p, text, re.IGNORECASE | re.MULTILINE)
        if match:
            scheme_name = match.group(1).strip()
            break
            
    issuing_authority = "Not clearly mentioned"
    auth_patterns = [
        r"(?:Ministry of|Department of|Government of|Govt\. of)\s+([^\n,.]+)",
        r"([^\n,.]+ (?:Authority|Council|Corporation|Ministry|Department))"
    ]
    for p in auth_patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            issuing_authority = match.group(0).strip()
            break
            
    website = "Not found"
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', text)
    if urls: website = urls[0]
    
    # 2. Indicators & Rules
    issues = []
    risk_points = 0
    
    # Rule: Unofficial Domain
    if website != "Not found":
        parsed = urlparse(website if website.startswith('http') else 'http://' + website)
        domain = parsed.netloc.lower()
        if domain and not (domain.endswith('.gov.in') or domain.endswith('.nic.in') or domain.endswith('.org.in')):
            if domain not in ['india.gov.in', 'mygov.in']: 
                issues.append("Unofficial website domain detected (non .gov.in)")
                risk_points += 35
        if any(short in domain for short in ['bit.ly', 't.co', 'tiny.cc', 'tinyurl']):
            issues.append("Suspicious shortened URL detected")
            risk_points += 40

    # Rule: Fee requests
    fee_keywords = ['fee', 'payment', 'charge', 'processing', 'deposit', 'advance', 'money']
    money_pattern = r"(?:Rs\.?|INR|\u20B9)\s?\d+|(?:\d+\s?(?:rupees|rs))"
    if any(k in text.lower() for k in fee_keywords) and re.search(money_pattern, text.lower()):
        issues.append("Document mentions processing fees or advance payments")
        risk_points += 45
        
    # Rule: Missing Identity
    if issuing_authority == "Not clearly mentioned":
        issues.append("Lack of clear government issuing authority")
        risk_points += 25
        
    # Rule: Contact Numbers
    phones = re.findall(r'[6-9]\d{9}', text)
    if phones and len(phones) > 0:
        issues.append("Uses individual mobile numbers for contact instead of official fixed lines")
        risk_points += 20

    # Rule: Urgent Language
    urgent_keywords = ['urgent', 'last chance', 'immediate', 'apply now', 'only today']
    if sum(1 for k in urgent_keywords if k in text.lower()) >= 2:
        issues.append("Uses high-pressure or urgent language typical of scams")
        risk_points += 15

    # 3. Cross-verification with Vector Store
    similarity_score = 0
    if vector_store:
        query = scheme_name if scheme_name != "Not detected clearly" else text[:300]
        results = vector_store.similarity_search_with_score(query, k=1)
        if results:
            doc, score = results[0]
            similarity_score = score
            if score > 0.9: # Weak match
                issues.append("Statement/Document content mismatch with official versions")
                risk_points += 40
            else:
                # Strong match lowers risk
                risk_points -= 20 

    # 4. Final Scoring and Status
    risk_pct = max(0, min(100, risk_points))
    correctness_pct = 100 - risk_pct
    
    if risk_pct > 70:
        status = "WRONG (PROBABLY FRAUDULENT)"
        level = "High Risk"
        recommendation = "AVOID applying. Report this message to 1930 (Cybercrime helpline)."
    elif risk_pct > 40:
        status = "SUSPICIOUS (CHECK CAREFULLY)"
        level = "Medium Risk"
        recommendation = "Verify via official portals like india.gov.in before sharing any data."
    elif risk_pct > 15:
        status = "UNVERIFIED"
        level = "Caution"
        recommendation = "Could not find a 100% match in our records. Exercise caution."
    else:
        status = "CORRECT (AUTHENTIC)"
        level = "Low Risk"
        recommendation = "This matches official records. Proceed as per guidelines."

    if not issues:
        issues = ["No suspicious indicators found. Statement aligns with official policy."]

    # 5. Formatted Output
    report = f"""
## Verification Summary: {status}

**Authenticity Score:** {correctness_pct}%
**Fraud Risk Score:** {risk_pct}%

---

**Scheme Identity:**
- **Name:** {scheme_name}
- **Authority:** {issuing_authority}
- **Website:** {website}

**Analysis Details:**
"""
    for issue in issues:
        report += f"• {issue}\n"
        
    report += f"\n**Recommendation:**\n{recommendation}"
    
    return level, status, report, risk_pct
