import os
from pypdf import PdfReader
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a Word document."""
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}")
    return text

def extract_text_from_txt(txt_path):
    """Extracts text from a plain text file."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {txt_path}: {e}")
        return ""

def extract_text(file_path):
    """General text extraction for supported formats."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf": return extract_text_from_pdf(file_path)
    if ext == ".docx": return extract_text_from_docx(file_path)
    if ext == ".txt": return extract_text_from_txt(file_path)
    return ""

def get_text_chunks(text):
    """Splits text into manageable chunks for RAG."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_quick_summary(text):
    """Provides a detailed, rule-based summary focusing on application steps."""
    lines = text.split('\n')
    summary = {
        "title": "Unknown Government Scheme",
        "highlights": [],
        "eligibility": "Refer to document for eligibility details.",
        "how_to_apply": [],
        "required_documents": [],
        "methods": [],
        "tracking": "Not specified in document.",
        "link": None,
        "category": "Social Welfare"
    }
    
    # Keywords for discovery
    highlight_keywords = ["benefit", "provide", "assistance", "subsidy", "financial", "grant", "allowance", "support", "covered", "incentive"]
    elig_keywords = ["eligible", "eligibility", "qualification", "criteria", "limit", "age", "income"]
    
    # 1. Title & Category Detection
    for line in lines[:20]:
        line_l = line.lower()
        if any(keyword in line for keyword in ["Scheme", "Policy", "Pradhan", "Yojana", "Mission"]):
            if len(line.strip()) > 5:
                summary["title"] = line.strip()
            # Category Detection
            if any(word in line_l for word in ["agriculture", "kisan", "farmer", "crop"]): summary["category"] = "Agriculture"
            elif any(word in line_l for word in ["health", "medical", "hospital", "ayushman"]): summary["category"] = "Healthcare"
            elif any(word in line_l for word in ["housing", "awas", "home"]): summary["category"] = "Housing"
            elif any(word in line_l for word in ["pension", "vaya", "elderly", "senior"]): summary["category"] = "Social Security"
            elif any(word in line_l for word in ["education", "student", "school", "scholarship"]): summary["category"] = "Education"
            break
            
    # --- NEW: Check if document is short enough to show EVERYTHING line-by-line ---
    # First, collect all substantial non-empty lines
    all_substantial_lines = []
    for line in lines:
        line_s = line.strip()
        if len(line_s) > 10 and "http" not in line_s.lower():
            if line_s not in all_substantial_lines:
                all_substantial_lines.append(line_s)
    
    # If the total number of points in the document is small (<= 25), show ALL of them
    if 0 < len(all_substantial_lines) <= 25:
        summary["highlights"] = all_substantial_lines
        # Also try to pick a title from the first line
        if summary["title"] == "Unknown Government Scheme" and all_substantial_lines:
            summary["title"] = all_substantial_lines[0][:100]
    else:
        # 2. Deep Extraction Loop for larger files
        seen_lines = set()
        for line in lines:
            l = line.lower().strip()
            if not l or len(l) < 5: continue
            if l in seen_lines: continue
            seen_lines.add(l)

            # Highlights - Capture up to 20 important points
            if any(w in l for w in highlight_keywords) and len(summary["highlights"]) < 20:
                if len(line.strip()) > 20:
                    summary["highlights"].append(line.strip())

            # Eligibility
            if any(w in l for w in elig_keywords):
                if len(line.strip()) > 15 and summary["eligibility"] == "Refer to document for eligibility details.":
                    summary["eligibility"] = line.strip()

            # Required Documents
            doc_keywords = ["aadhaar", "pan card", "income certificate", "ration card", "voter id", "passport", "certificate", "proof", "photograph"]
            if any(w in l for w in doc_keywords) and len(summary["required_documents"]) < 10:
                cleaned = line.strip().lstrip('•-*1234567890. ')
                if 5 < len(cleaned) < 120 and cleaned not in summary["required_documents"]:
                    summary["required_documents"].append(cleaned)

            # Application Methods
            if "online" in l or "portal" in l or "website" in l:
                if "Online Application" not in summary["methods"]: summary["methods"].append("Online Application")
            if "offline" in l or "office" in l or "center" in l or "csc" in l:
                if "Offline / Government Center" not in summary["methods"]: summary["methods"].append("Offline / Government Center")

            # Application Steps
            step_keywords = ["step", "procedure", "how to apply", "registration", "visit", "apply"]
            if any(w in l for w in step_keywords) and len(summary["how_to_apply"]) < 8:
                cleaned_step = line.strip().lstrip('•-*1234567890. ')
                if 15 < len(cleaned_step) < 250 and cleaned_step not in summary["how_to_apply"]:
                    summary["how_to_apply"].append(cleaned_step)

            # Tracking
            if any(w in l for w in ["track", "status", "application id", "reference number"]) and (summary["tracking"] == "Not specified in document." or len(summary["tracking"]) < 10):
                summary["tracking"] = line.strip()

            # Link Extraction
            if "http" in l or "https" in l or ".gov.in" in l:
                import re
                links = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', line)
                if links:
                    gov_links = [link for link in links if ".gov.in" in link]
                    summary["link"] = gov_links[0] if gov_links else links[0]

    # --- Robust Fallback for empty highlights/eligibility in large files ---
    if not summary["highlights"] and len(all_substantial_lines) > 0:
        summary["highlights"] = all_substantial_lines[:20]

    if summary["eligibility"] == "Refer to document for eligibility details." and len(lines) > 5:
        candidates = [l.strip() for l in lines[:30] if 20 < len(l.strip()) < 150]
        if candidates:
            summary["eligibility"] = candidates[0]

    if not summary["how_to_apply"]:
        summary["how_to_apply"] = ["Refer to the official portal for detailed steps.", "Consult the nearest government administrative office."]

    return summary

def process_policy_docs(directory):
    """Iterates through a directory and processes all supported documents."""
    all_chunks = []
    file_metadata = []
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    for filename in os.listdir(directory):
        ext = os.path.splitext(filename)[1].lower()
        if ext in [".pdf", ".docx", ".txt"]:
            path = os.path.join(directory, filename)
            text = extract_text(path)
            chunks = get_text_chunks(text)
            all_chunks.extend(chunks)
            for _ in chunks:
                file_metadata.append({"source": filename})
                
    return all_chunks, file_metadata
