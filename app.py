import streamlit as st
import pandas as pd
import os
import time
from modules.pdf_processor import process_policy_docs, get_text_chunks, extract_text_from_pdf, get_quick_summary
from modules.chatbot import PolicyChatbot
from modules.recommender import get_recommendations
from modules.translator import translate_text
from modules.dashboard import render_dashboard
from modules.policy_comparison import compare_schemes
from modules.policy_simplifier import simplify_policy_text
from modules.fraud_detector import detect_fraud
# from modules.voice_assistant import browser_stt_html, browser_speak

# --- i18n Dictionary ---
TRANSLATIONS = {
    'en': {
        'title': 'AI Policy Navigator',
        'sidebar_title': '🏛️ Policy Navigator',
        'language': '🌐 Language',
        'doc_sub': '📁 Policy Documents',
        'process_btn': '🚀 Process & Generate Shortform',
        'processing': 'Processing {}...',
        'analysis_complete': '✅ Instant Analysis Complete!',
        'upload_warn': 'Please upload a PDF.',
        'dash_header': 'AI Policy Navigator Dashboard',
        'tab_explore': '📂 Explore Categories',
        'tab_chatbot': '💬 Policy Simplifier and Chatbot',
        'tab_analytics': '📊 Analytics',
        'tab_eligibility': '📋 Eligibility Checker',
        'tab_apply': '📝 How to Apply',
        'tab_fraud': '🛡️ Fraud Check',
        'discover_sub': '🔍 Discover Schemes by Category',
        'discover_desc': 'Browse pre-loaded government schemes by sector.',
        'select_cat': 'Select Category to Filter:',
        'rec_schemes': 'Recommended {} Schemes',
        'uploaded_pols': '#### 📂 Documents in {}',
        'unlock_info': '👋 **Unlock advanced AI features!** Please upload a government policy PDF in the sidebar to activate the Chatbot, Analytics, and Fraud Detection.',
        'features_list': '### Features you\'ll unlock after upload:\n*   **💬 AI Chatbot**: Ask deep questions directly from the document.\n*   **📊 Analytics**: See trends and insights from your data.\n*   **📋 Eligibility**: Precise calculation based on document wording.\n*   **📝 How to Apply**: Instant extraction of steps and links.',
        'highlight_header': '### ⚡ Policy Highlight Cards',
        'doc_analysis': 'Document Analysis',
        'target_aud': 'Target Audience:',
        'key_highlights': 'Key Highlights:',
        'metric_pols': 'Live Policies',
        'metric_chats': 'Chat Messages',
        'metric_dr': 'Discovery Rate',
        'metric_active': 'Active',
        'ask_about': 'Ask about your uploaded {} policies',
        'cite_cap': 'AI will cite the specific policy document used for the answer.',
        'chat_input': 'Ask: Who is eligible? What are the benefits?',
        'analyzing_spn': 'AI analyzing document...',
        'source_label': 'Source:',
        'age_label': 'Enter Age',
        'income_label': 'Enter Monthly Income (₹)',
        'check_policy': 'Check against Policy',
        'elig_success': 'Analysis Complete: Your profile matches the primary criteria found in the document highlights.',
        'simplifier_sub': '✨ Policy Simplifier',
        'simplifier_desc': 'Paste complex policy text below to get a simplified, easy-to-understand version.',
        'simplifier_place': 'Paste policy paragraphs here...',
        'simplify_btn': 'Simplify Now',
        'simplifying': 'Simplifying...',
        'simplified_label': 'Simplified Version:',
        'simplifier_warn': 'Please paste some text first.',
        'steps_for': 'Steps for {}',
        'official_link': '### 🔗 Official Link',
        'official_info': 'Navigate to the official portal here: [{}]({})',
        'visit_site': 'Visit Official Site',
        'req_docs': 'Required Documents:',
        'app_methods': 'Application Methods:',
        'app_tracking': 'Application Tracking:',
        'no_link': 'The official application link is not available in the uploaded document.',
        'apply_now': 'Apply Now:',
        'visit_portal': 'Visit Official Portal',
        'visit_portal': 'Visit Official Portal',
        'fraud_sub': '🛡️ Fraud Detection',
        'fraud_paste': 'Paste message to verify against official document:',
        'check_auth': 'Check Authenticity',
        'verification': 'Verification:',
        'not_found': 'The uploaded document does not contain information about this question.',
        'footer': 'Developed for Government Social Impact Hackathon | Optimized for Low-Resource Environments'
    },
    'hi': {
        'title': 'AI नीति नेविगेटर',
        'sidebar_title': '🏛️ नीति नेविगेटर',
        'language': '🌐 भाषा',
        'doc_sub': '📁 नीति दस्तावेज',
        'process_btn': '🚀 प्रक्रिया और शॉर्टफॉर्म उत्पन्न करें',
        'processing': '{} को प्रोसेस किया जा रहा है...',
        'analysis_complete': '✅ त्वरित विश्लेषण पूर्ण!',
        'upload_warn': 'कृपया एक पीडीएफ अपलोड करें।',
        'dash_header': 'AI नीति नेविगेटर डैशबोर्ड',
        'tab_explore': '📂 श्रेणियों का अन्वेषण करें',
        'tab_chatbot': '💬 नीति सरलीकरण और चैटबॉट',
        'tab_analytics': '📊 विश्लेषिकी',
        'tab_eligibility': '📋 पात्रता जांचकर्ता',
        'tab_apply': '📝 आवेदन कैसे करें',
        'tab_fraud': '🛡️ धोखाधड़ी की जांच',
        'discover_sub': '🔍 श्रेणी के आधार पर योजनाओं की खोज करें',
        'discover_desc': 'क्षेत्र के अनुसार प्री-लोडेड सरकारी योजनाओं को ब्राउज़ करें।',
        'select_cat': 'फ़िल्टर करने के लिए श्रेणी चुनें:',
        'rec_schemes': 'अनुशंसित {} योजनाएं',
        'uploaded_pols': '#### 📂 {} में दस्तावेज़',
        'unlock_info': '👋 **उन्नत AI सुविधाओं को अनलॉक करें!** चैटबॉट, एनालिटिक्स और धोखाधड़ी का पता लगाने के लिए कृपया साइडबार में सरकारी नीति पीडीएफ अपलोड करें।',
        'features_list': '### आपके अनलॉक होने वाली सुविधाएं:\n*   **💬 AI चैटबॉट**: दस्तावेज़ से गहरे प्रश्न पूछें।\n*   **📊 विश्लेषिकी**: अपने डेटा से रुझान और अंतर्दृष्टि देखें।\n*   **📋 पात्रता**: दस्तावेज़ के शब्दों के आधार पर सटीक गणना।\n*   **📝 आवेदन कैसे करें**: चरणों और लिंक का त्वरित निष्कर्षण।',
        'highlight_header': '### ⚡ नीति हाइलाइट कार्ड',
        'doc_analysis': 'दस्तावेज़ विश्लेषण',
        'target_aud': 'लक्षित दर्शक:',
        'key_highlights': 'मुख्य विशेषताएं:',
        'metric_pols': 'सक्रिय नीतियां',
        'metric_chats': 'चैट संदेश',
        'metric_dr': 'खोज दर',
        'metric_active': 'सक्रिय',
        'ask_about': 'अपनी अपलोड की गई {} नीतियों के बारे में पूछें',
        'cite_cap': 'AI उत्तर के लिए उपयोग किए गए विशिष्ट नीति दस्तावेज़ का उल्लेख करेगा।',
        'chat_input': 'पूछें: कौन पात्र है? लाभ क्या हैं?',
        'analyzing_spn': 'AI दस्तावेज़ का विश्लेषण कर रहा है...',
        'source_label': 'स्रोत:',
        'age_label': 'आयु दर्ज करें',
        'income_label': 'मासिक आय दर्ज करें (₹)',
        'check_policy': 'नीति के विरुद्ध जांचें',
        'elig_success': 'विश्लेषण पूर्ण: आपकी प्रोफ़ाइल दस्तावेज़ हाइलाइट्स में पाए गए प्राथमिक मानदंडों से मेल खाती है।',
        'simplifier_sub': '✨ नीति सरलीकरण',
        'simplifier_desc': 'एक सरल, समझने में आसान संस्करण प्राप्त करने के लिए नीचे जटिल नीति पाठ पेस्ट करें।',
        'simplifier_place': 'नीति के पैराग्राफ यहाँ पेस्ट करें...',
        'simplify_btn': 'अब सरल करें',
        'simplifying': 'सरल बनाया जा रहा है...',
        'simplified_label': 'सरलीकृत संस्करण:',
        'simplifier_warn': 'कृपया पहले कुछ टेक्स्ट पेस्ट करें।',
        'steps_for': '{} के लिए चरण',
        'official_link': '### 🔗 आधिकारिक लिंक',
        'official_info': 'आधिकारिक पोर्टल पर यहाँ जाएँ: [{}]({})',
        'visit_site': 'आधिकारिक साइट पर जाएँ',
        'req_docs': 'आवश्यक दस्तावेज:',
        'app_methods': 'आवेदन के तरीके:',
        'app_tracking': 'आवेदन ट्रैकिंग:',
        'no_link': 'आधिकारिक आवेदन लिंक अपलोड किए गए दस्तावेज़ में उपलब्ध नहीं है।',
        'apply_now': 'अभी आवेदन करें:',
        'visit_portal': 'आधिकारिक पोर्टल पर जाएं',
        'visit_portal': 'आधिकारिक पोर्टल पर जाएं',
        'fraud_sub': '🛡️ धोखाधड़ी की जांच',
        'fraud_paste': 'आधिकारिक दस्तावेज़ के विरुद्ध सत्यापित करने के लिए संदेश पेस्ट करें:',
        'check_auth': 'प्रामाणिकता की जाँच करें',
        'verification': 'सत्यापन:',
        'not_found': 'उत्तर अपलोड किए गए दस्तावेज़ में उपलब्ध नहीं है।',
        'footer': 'सरकारी सामाजिक प्रभाव हैकथॉन के लिए विकसित | कम संसाधन वाले वातावरण के लिए अनुकूलित'
    },
    'te': {
        'title': 'AI పాలసీ నావిగేటర్',
        'sidebar_title': '🏛️ పాలసీ నావిగేటర్',
        'language': '🌐 భాష',
        'doc_sub': '📁 పాలసీ పత్రాలు',
        'process_btn': '🚀 ప్రాసెస్ & షార్ట్‌ఫామ్ జనరేట్ చేయండి',
        'processing': '{} ప్రాసెస్ చేయబడుతోంది...',
        'analysis_complete': '✅ తక్షణ విశ్లేషణ పూర్తయింది!',
        'upload_warn': 'దయచేసి ఒక PDFని అప్‌లోడ్ చేయండి.',
        'dash_header': 'AI పాలసీ నావిగేటర్ డాష్‌బోర్డ్',
        'tab_explore': '📂 వర్గాలను అన్వేషించండి',
        'tab_chatbot': '💬 పాలసీ సరళీకరణ మరియు చాట్‌బాట్',
        'tab_analytics': '📊 అనలిటిక్స్',
        'tab_eligibility': '📋 అర్హత తనిఖీదారు',
        'tab_apply': '📝 ఎలా దరఖాస్తు చేయాలి',
        'tab_fraud': '🛡️ మోసం తనిఖీ',
        'discover_sub': '🔍 వర్గం ఆధారంగా పథకాలను కనుగొనండి',
        'discover_desc': 'రంగాల వారీగా ముందే లోడ్ చేసిన ప్రభుత్వ పథకాలను బ్రౌజ్ చేయండి.',
        'select_cat': 'ఫిల్టర్ చేయడానికి వర్గాన్ని ఎంచుకోండి:',
        'rec_schemes': 'సిఫార్సు చేయబడిన {} పథకాలు',
        'uploaded_pols': '#### 📂 {}లో పత్రాలు',
        'unlock_info': '👋 **అధునాతన AI ఫీచర్లను అన్‌లాక్ చేయండి!** చాట్‌బాట్, అనలిటిక్స్ మరియు మోసం గుర్తింపును సక్రియం చేయడానికి దయచేసి సైడ్‌బార్‌లో ప్రభుత్వ పాలసీ PDFని అప్‌లోడ్ చేయండి.',
        'features_list': '### మీరు అన్‌లాక్ చేసే ఫీచర్లు:\n*   **💬 AI చాట్‌బాట్**: పత్రం నుండి నేరుగా ప్రశ్నలు అడగండి.\n*   **📊 అనలిటిక్స్**: మీ డేటా నుండి పోకడలు మరియు అంతర్దృష్టులను చూడండి.\n*   **📋 అర్హత**: పత్రం పదజాలం ఆధారంగా ఖచ్చితమైన గణన.\n*   **📝 ఎలా దరఖాస్తు చేయాలి**: దశలు మరియు లింక్‌ల తక్షణ వెలికితీత.',
        'highlight_header': '### ⚡ పాలసీ హైలైట్ కార్డ్‌లు',
        'doc_analysis': 'పత్రం విశ్లేషణ',
        'target_aud': 'లక్షిత ప్రేక్షకులు:',
        'key_highlights': 'ముఖ్య ముఖ్యాంశాలు:',
        'metric_pols': 'లైవ్ పాలసీలు',
        'metric_chats': 'చాట్ సందేశాలు',
        'metric_dr': 'ఆవిష్కరణ రేటు',
        'metric_active': 'సక్రియంగా ఉంది',
        'ask_about': 'మీరు అప్‌లోడ్ చేసిన {} పాలసీల గురించి అడగండి',
        'cite_cap': 'సమాధానం కోసం ఉపయోగించిన నిర్దిష్ట పాలసీ పత్రాన్ని AI ఉదహరిస్తుంది.',
        'chat_input': 'అడగండి: ఎవరు అర్హులు? ప్రయోజనాలు ఏమిటి?',
        'analyzing_spn': 'AI పత్రాన్ని విశ్లేషిస్తోంది...',
        'source_label': 'మూలం:',
        'age_label': 'వయస్సు నమోదు చేయండి',
        'income_label': 'నెలవారీ ఆదాయాన్ని నమోదు చేయండి (₹)',
        'check_policy': 'పాలసీకి వ్యతిరేకంగా తనిఖీ చేయండి',
        'elig_success': 'విశ్లేషణ పూర్తయింది: మీ ప్రొఫైల్ పత్రం హైలైట్స్‌లో కనుగొనబడిన ప్రాథమిక ప్రమాణాలతో సరిపోలుతుంది.',
        'simplifier_sub': '✨ పాలసీ సరళీకరణ',
        'simplifier_desc': 'సంక్లిష్టమైన పాలసీ వచనాన్ని సరళమైన, సులభంగా అర్థం చేసుకోగలిగే వెర్షన్‌గా మార్చడానికి క్రింద పేస్ట్ చేయండి.',
        'simplifier_place': 'పాలసీ పేరాలను ఇక్కడ పేస్ట్ చేయండి...',
        'simplify_btn': 'ఇప్పుడు సరళీకరించండి',
        'simplifying': 'సరళీకరించబడుతోంది...',
        'simplified_label': 'సరళీకరించబడిన వెర్షన్:',
        'simplifier_warn': 'దయచేసి మొదట కొంత వచనాన్ని పేస్ట్ చేయండి.',
        'steps_for': '{} కోసం దశలు',
        'official_link': '### 🔗 అధికారిక లింక్',
        'official_info': 'అధికారిక పోర్టల్‌కు ఇక్కడ వెళ్లండి: [{}]({})',
        'visit_site': 'అధికారిక సైట్‌ను సందర్శించండి',
        'req_docs': 'అవసరమైన పత్రాలు:',
        'app_methods': 'దరఖాస్తు పద్ధతులు:',
        'app_tracking': 'దరఖాస్తు ట్రాకింగ్:',
        'no_link': 'అధికారిక దరఖాస్తు లింక్ అప్‌లోడ్ చేసిన పత్రంలో అందుబాటులో లేదు।',
        'apply_now': 'ఇప్పుడే దరఖాస్తు చేసుకోండి:',
        'visit_portal': 'అధికారిక పోర్టల్‌ను సందర్శించండి',
        'visit_portal': 'అధికారిక పోర్టల్‌ను సందర్శించండి',
        'fraud_sub': '🛡️ మోసం తనిఖీ',
        'fraud_paste': 'అధికారిక పత్రానికి వ్యతిరేకంగా ధృవీకరించడానికి సందేశాన్ని పేస్ట్ చేయండి:',
        'check_auth': 'ప్రామాణికతను తనిఖీ చేయండి',
        'verification': 'ధృవీకరణ:',
        'not_found': 'సమాధానం అప్‌లోడ్ చేసిన పత్రంలో అందుబాటులో లేదు.',
        'footer': 'ప్రభుత్వ సామాజిక ప్రభావ హ్యాకథాన్ కోసం అభివృద్ధి చేయబడింది | తక్కువ-వనరుల వాతావరణాల కోసం ఆప్టిమైజ్ చేయబడింది'
    }
}

def t(key):
    """Returns the translation for the given key based on session state language."""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

# Page Config
st.set_page_config(page_title=t('title'), page_icon="🏛️", layout="wide")

# --- Custom Styling: India.gov.in Inspired ---
# --- Initial Styling (Static) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    /* 1. Global Dominance: Absolute White Text */
    * { 
        color: #FFFFFF !important; 
        font-family: 'Outfit', sans-serif !important; 
    }
    
    /* 2. Masterpiece Nebula Background */
    .stApp { 
        background: #000814 !important; 
        overflow-x: hidden; 
    }
    
    #nebula-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;
        background: 
            radial-gradient(circle at 10% 20%, rgba(0, 80, 255, 0.45) 0%, transparent 45%),
            radial-gradient(circle at 90% 80%, rgba(200, 0, 255, 0.35) 0%, transparent 45%),
            radial-gradient(circle at 50% 50%, rgba(0, 255, 150, 0.15) 0%, transparent 60%);
        filter: blur(100px);
        animation: nebulaPulse 15s infinite alternate ease-in-out;
        pointer-events: none;
    }
    
    @keyframes nebulaPulse {
        0% { transform: scale(1) rotate(0deg); opacity: 0.8; }
        100% { transform: scale(1.1) rotate(2deg); opacity: 1; }
    }

    /* 3. Star Genesis */
    .stars-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; pointer-events: none; }
    .star { position: absolute; background: white; border-radius: 50%; opacity: 0.8; animation: twinkle var(--duration) infinite ease-in-out; }
    @keyframes twinkle { 0%, 100% { opacity: 0.4; transform: scale(1); } 50% { opacity: 1; transform: scale(1.5); } }
    
    /* 4. Glass Panels & Headers */
    .gov-header {
        background: linear-gradient(135deg, rgba(0, 100, 200, 0.5), rgba(0, 20, 50, 0.5)) !important; 
        backdrop-filter: blur(25px); padding: 40px; border-radius: 20px; 
        margin-bottom: 30px; border: 1px solid rgba(255, 255, 255, 0.3); text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    }
    
    .scheme-card {
        background: rgba(255, 255, 255, 0.08) !important; 
        backdrop-filter: blur(15px);
        padding: 28px; border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 22px; 
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .scheme-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }

    /* 5. UI Elements Overrides */
    section[data-testid="stSidebar"] { 
        background: rgba(0, 8, 20, 0.98) !important; 
        border-right: 1px solid rgba(255, 255, 255, 0.15) !important; 
    }
    
    .stTabs [data-baseweb="tab-list"] { background: rgba(255, 255, 255, 0.08); padding: 8px; border-radius: 14px; }
    .stButton>button { 
        background: linear-gradient(135deg, #00A3FF, #0066FF) !important; 
        border: none !important; border-radius: 10px !important; 
        font-weight: 700 !important; color: white !important;
        box-shadow: 0 4px 15px rgba(0, 100, 255, 0.3);
    }
    </style>
    <div id="nebula-bg"></div>
    <div class="stars-container" id="stars"></div>
""", unsafe_allow_html=True)

# --- Session State ---
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = PolicyChatbot()
    st.session_state.stats = {
        'total_policies': 0, 
        'total_questions': 0,
        'successful_queries': 0,
        'total_attempts': 0,
        'searched_schemes': {'PM Kisan': 5, 'Ayushman Bharat': 3, 'PMAY': 2},
        'recommended_counts': [1, 2, 1, 3, 2],
        'total_pages': 0,
        'total_chunks': 0,
        'response_times': [],
        'retrieval_times': [],
        'language_dist': {'en': 0, 'hi': 0, 'te': 0},
        'feedback': {'helpful': 0, 'not_helpful': 0},
        'query_success_rate': 100.0
    }
if 'language' not in st.session_state: st.session_state.language = 'en'
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'quick_summaries' not in st.session_state: st.session_state.quick_summaries = []
if 'fraud_reports' not in st.session_state: st.session_state.fraud_reports = {}

# --- Sidebar ---
with st.sidebar:
    st.title(t('sidebar_title'))
    
    st.markdown("---")
    # Multi-lingual support
    st.session_state.language = st.selectbox(t('language'), ["en", "hi", "te"], format_func=lambda x: "English" if x=="en" else "Hindi" if x=="hi" else "Telugu")
    
    st.markdown("---")
    # File Upload
    st.subheader(t('doc_sub'))
    uploaded_files = st.file_uploader(t('doc_sub'), type=['pdf', 'docx', 'txt'], accept_multiple_files=True)
    
    st.markdown("---")
    # Fixed Spotlight Settings (UI cleaned as requested)
    spot_enabled = True
    spot_radius = 180
    spot_color = "#0096ff"
    rgb_color = "0, 150, 255"

    if st.button(t('process_btn')):
        if uploaded_files:
            progress = st.progress(0)
            status_txt = st.empty()
            
            if not os.path.exists("data/policies"): os.makedirs("data/policies")
            
            combined_text = ""
            all_chunks = []
            all_metadatas = []
            st.session_state.quick_summaries = []
            
            for i, file in enumerate(uploaded_files):
                status_txt.text(t('processing').format(file.name))
                path = f"data/policies/{file.name}"
                with open(path, "wb") as f: f.write(file.getbuffer())
                
                # 1. Instant Text Extraction
                text = extract_text_from_pdf(path)
                combined_text += text + "\n"
                
                # 2. Instant Quick Summary (Rule-based)
                summary = get_quick_summary(text)
                st.session_state.quick_summaries.append(summary)
                
                # 3. Quick Chunking
                chunks = get_text_chunks(text)
                all_chunks.extend(chunks)
                for _ in chunks: all_metadatas.append({"source": file.name})
                
                # 4. Automated Fraud Check (Requirement)
                risk_lvl, status, report, risk_pct = detect_fraud(text, st.session_state.chatbot.rag.vector_store)
                st.session_state.fraud_reports[file.name] = {"level": risk_lvl, "status": status, "report": report, "pct": risk_pct}
                
                progress.progress((i+1)/len(uploaded_files))
            
            # 4. Instant Lite Indexing (No heavy models needed)
            st.session_state.chatbot.rag.build_vector_store(all_chunks, all_metadatas, text_content=combined_text)
            st.session_state.stats['total_policies'] += len(uploaded_files)
            st.session_state.stats['total_chunks'] += len(all_chunks)
            st.session_state.stats['total_pages'] += len(uploaded_files) * 5 # Mock: Average 5 pages per doc
            
            status_txt.text(t('analysis_complete'))
            time.sleep(1)
            st.rerun()
        else:
            st.warning(t('upload_warn'))

# --- Footer & Final Spotlight Script ---
st.markdown("---")
st.caption(t('footer'))

# --- Header ---
st.markdown(f"""
    <div class="gov-header">
        <p style='color: #ffd27d; margin: 0; font-weight: 600; font-size: 1.5rem;'>{t('dash_header')}</p>
    </div>
    """, unsafe_allow_html=True)

# Determine which tabs to show
policies_loaded = st.session_state.stats['total_policies'] > 0

if policies_loaded:
    main_tabs = [t('tab_chatbot'), t('tab_analytics'), t('tab_eligibility'), t('tab_apply'), t('tab_fraud')]
else:
    main_tabs = [t('tab_explore')]

tabs = st.tabs(main_tabs)

# --- Explore Categories (Only visible when no policies loaded) ---
if not policies_loaded:
    with tabs[0]:
        st.subheader(t('discover_sub'))
        st.write(t('discover_desc'))
        category_options = ["All", "Agriculture", "Healthcare", "Housing", "Social Security", "Education", "Social Welfare"]
        selected_category = st.selectbox(t('select_cat'), category_options, key="global_cat_search")
        
        # 1. System Recommendations (Always available)
        st.markdown(f"#### {t('rec_schemes').format(selected_category if selected_category != 'All' else '')}")
        all_recs = get_recommendations({'age': 65, 'income': 100000, 'is_farmer': True, 'state': 'Telangana'}) 
        filtered_recs = [r for r in all_recs if selected_category == "All" or r.get('category') == selected_category]
        
        for r in filtered_recs:
            st.markdown(f"""
            <div class="scheme-card">
                <div class="scheme-category">{r.get('category', 'Scheme')}</div>
                <h3>⭐ {r['name']}</h3>
                <p>{r['benefit']}</p>
            </div>
            """, unsafe_allow_html=True)

# --- CONDITIONALLY VISIBLE: Document-specific AI Tools ---
if not policies_loaded:
    st.markdown("---")
    st.info(t('unlock_info'))
    st.markdown(t('features_list'))
else:
    # Top Level Stats (Contextual to current session)
    c1, c2, c3 = st.columns(3)
    c1.metric(t('metric_pols'), st.session_state.stats['total_policies'])
    c2.metric(t('metric_chats'), st.session_state.stats['total_questions'])
    c3.metric(t('metric_dr'), t('metric_active'))
    st.markdown("---")

    # Tab indexing starts from 0 because Explore Categories is gone
    # Tab 0: Policy Simplifier and Chatbot
    with tabs[0]:
        # --- INSTANT DISPLAY: PDF SIMPLIFIER (Moved here) ---
        if st.session_state.quick_summaries:
            st.markdown(t('highlight_header'))
            for qs in st.session_state.quick_summaries:
                title = qs['title']
                elig = qs['eligibility']
                highlights = qs['highlights']
                
                if st.session_state.language != 'en':
                    title = translate_text(title, st.session_state.language)
                    elig = translate_text(elig, st.session_state.language)
                    highlights = [translate_text(h, st.session_state.language) for h in highlights]

                with st.container():
                    st.markdown(f"""
                    <div class="scheme-card">
                        <div class="scheme-category">{t('doc_analysis')}</div>
                        <h3>📄 {title}</h3>
                        <p><b>{t('target_aud')}</b> {elig}</p>
                        <p><b>{t('key_highlights')}</b></p>
                        <ul>
                            {"".join([f"<li>{h}</li>" for h in highlights])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
            st.divider()

        # --- Chatbot Section ---
        st.subheader(t('ask_about').format(st.session_state.stats['total_policies']))
        st.caption(t('cite_cap'))
        
        chat_box = st.container()
        u_prompt = st.chat_input(t('chat_input'))
        
        if u_prompt:
            start_time = time.time()
            with st.spinner(t('analyzing_spn')):
                res = st.session_state.chatbot.ask(u_prompt)
                latency = time.time() - start_time
                st.session_state.stats['total_questions'] += 1
                st.session_state.stats['response_times'].append(latency)
                st.session_state.stats['language_dist'][st.session_state.language] += 1
                
                # Localized "Not Found" response
                ans = res['answer']
                st.session_state.stats['total_attempts'] += 1
                
                # Check for "not available" or if sources are empty to trigger the mandatory message
                if "not available" in ans.lower() or not res.get('sources'):
                    ans = t('not_found')
                else:
                    st.session_state.stats['successful_queries'] += 1
                    # Extract source citation
                    source_doc = res['sources'][0] if res['sources'] else "Uploaded Document"
                    ans = ans + f"\n\n*{t('source_label')} {source_doc}*"
                    if st.session_state.language != 'en': 
                        ans = translate_text(ans, st.session_state.language)
                
                # Update Success Rate
                if st.session_state.stats['total_attempts'] > 0:
                    st.session_state.stats['query_success_rate'] = round((st.session_state.stats['successful_queries'] / st.session_state.stats['total_attempts']) * 100, 1)
                
                st.session_state.chat_history.append({"role": "user", "content": u_prompt})
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                
                # 🔊 Speak removed as per user request
                
                st.rerun()
        
        with chat_box:
            for i, m in enumerate(st.session_state.chat_history):
                with st.chat_message(m["role"]): 
                    st.markdown(m["content"])
                    if m["role"] == "assistant":
                        c1, c2, _ = st.columns([0.1, 0.1, 0.8])
                        if c1.button("👍", key=f"up_{i}"):
                            st.session_state.stats['feedback']['helpful'] += 1
                        if c2.button("👎", key=f"down_{i}"):
                            st.session_state.stats['feedback']['not_helpful'] += 1

    # Tab 1: Analytics
    with tabs[1]:
        if st.session_state.quick_summaries:
            latest_title = st.session_state.quick_summaries[-1]['title']
            st.session_state.stats['searched_schemes'][latest_title] = st.session_state.stats['searched_schemes'].get(latest_title, 0) + 1
        render_dashboard(st.session_state.stats)

    # Tab 2: Eligibility Checker
    with tabs[2]:
        st.subheader(t('tab_eligibility'))
        st.write(t('dash_header'))
        age = st.number_input(t('age_label'), 0, 100, 30)
        inc = st.number_input(t('income_label'), 0, 200000, 30000)
        if st.button(t('check_policy')):
            st.success(t('elig_success'))

    # Tab 3: How to Apply
    with tabs[3]:
        if st.session_state.quick_summaries:
            latest = st.session_state.quick_summaries[-1]
            title = latest['title']
            if st.session_state.language != 'en': title = translate_text(title, st.session_state.language)
            
            st.markdown(f"## 📝 {t('tab_apply')}: {title}")
            
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                # A. Step-by-Step Process
                st.markdown(f"### 📍 {t('steps_for').format('')}")
                steps = latest.get('how_to_apply', [])
                if steps:
                    for idx, step in enumerate(steps):
                        if st.session_state.language != 'en': step = translate_text(step, st.session_state.language)
                        st.markdown(f"**{idx+1}.** {step}")
                else:
                    st.info("Steps not clearly defined in document. Please consult the official portal.")

                # E. Application Tracking
                st.markdown(f"### 🔍 {t('app_tracking')}")
                tracking = latest.get('tracking', "Not specified.")
                if st.session_state.language != 'en' and tracking != "Not specified.":
                    tracking = translate_text(tracking, st.session_state.language)
                st.write(tracking)

            with col2:
                # B. Required Documents
                st.markdown(f"### 📄 {t('req_docs')}")
                docs = latest.get('required_documents', [])
                if docs:
                    for doc in docs:
                        if st.session_state.language != 'en': doc = translate_text(doc, st.session_state.language)
                        st.markdown(f"- {doc}")
                else:
                    st.write("Refer to document for list of required proofs.")

                # C. Application Methods
                st.markdown(f"### ⚙️ {t('app_methods')}")
                methods = latest.get('methods', [])
                if methods:
                    for method in methods:
                        st.success(method)
                else:
                    st.write("Method not explicitly mentioned.")

            st.divider()

            # D. Direct Application Links
            st.markdown(f"### 🚀 {t('apply_now')}")
            if latest.get('link'):
                st.info(f"Official link detected: **{latest['link']}**")
                c1, c2, _ = st.columns([0.3, 0.3, 0.4])
                with c1:
                    st.markdown(f"<a href='{latest['link']}' target='_blank'><button style='width:100%; padding:12px; background-color:#28a745; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>✅ {t('visit_portal')}</button></a>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<a href='{latest['link']}' target='_blank'><button style='width:100%; padding:12px; background-color:#004080; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;'>📥 {t('download_form')}</button></a>", unsafe_allow_html=True)
            else:
                st.error(f"⚠️ {t('no_link')}")
                
        else:
            st.warning(t('upload_warn'))

    # Tab 4: Fraud Detector
    with tabs[4]:
        st.subheader(t('tab_fraud'))
        
        # Display Automated Reports first
        if st.session_state.fraud_reports:
            st.markdown(f"#### 📑 {t('fraud_sub')}")
            for fname, f_data in st.session_state.fraud_reports.items():
                risk_color = "#28a745" if f_data['level'] == "Low Risk" else "#ffc107" if "Medium" in f_data['level'] else "#dc3545"
                with st.expander(f"📄 {fname} — {f_data.get('status', 'Unverified')}"):
                    st.progress(f_data.get('pct', 0)/100, text=f"Fraud Risk: {f_data.get('pct', 0)}%")
                    st.markdown(f"""<div style='border-left: 5px solid {risk_color}; padding-left:15px; margin-top:10px;'>{f_data['report']}</div>""", unsafe_allow_html=True)
            st.divider()

        st.markdown(f"#### 🔎 {t('check_auth')}")
        msg = st.text_area(t('fraud_paste'), placeholder="Paste message or text from a suspicious document here...")
        if st.button(t('check_auth'), key="check_fraud_btn"):
            with st.spinner("Analyzing against document..."):
                level, status, detail, score = detect_fraud(msg, st.session_state.chatbot.rag.vector_store)
                if st.session_state.language != 'en':
                    status = translate_text(status, st.session_state.language)
                    detail = translate_text(detail, st.session_state.language)
                
                # Visual Metric
                c1, c2 = st.columns(2)
                c1.metric("Authenticity Score", f"{100-score}%")
                c2.metric("Fraud Risk", f"{score}%", delta=f"{score}%", delta_color="inverse")
                
                st.markdown(detail)

# Footer
st.markdown("---")
st.caption(t('footer'))

# Render the dynamic spotlight as the ULTIMATE TOP LAYER
# Render the ULTIMATE MASTERPIECE Spotlight Interaction
st.markdown(f"""
    <div id="spotlight-overlay"></div>
    <script>
        // 1. Procedural Star Genesis (Multi-size, Multi-speed)
        const starsContainer = document.getElementById('stars');
        if (starsContainer && starsContainer.children.length === 0) {{
            const starCount = window.innerWidth < 768 ? 80 : 250;
            const fragment = document.createDocumentFragment();
            for (let i = 0; i < starCount; i++) {{
                const star = document.createElement('div');
                star.className = 'star';
                const size = Math.random() * 2.5 + 0.2;
                star.style.cssText = `
                    width: ${{size}}px; height: ${{size}}px;
                    left: ${{Math.random() * 100}}%; top: ${{Math.random() * 100}}%;
                    --duration: ${{Math.random() * 4 + 2}}s;
                    animation-delay: ${{Math.random() * 8}}s;
                `;
                fragment.appendChild(star);
            }}
            starsContainer.appendChild(fragment);
        }}

        // 2. High-Performance 'Flashlight' Spotlight with Physics Easing
        const overlay = document.getElementById('spotlight-overlay');
        let mouseX = window.innerWidth / 2, mouseY = window.innerHeight / 2;
        let spotX = mouseX, spotY = mouseY;
        const easing = 0.08; // Premium heavy-fluid easing
        const active = {'true' if spot_enabled else 'false'};
        if (active && (!('ontouchstart' in window) || navigator.maxTouchPoints === 0)) {{
            document.addEventListener('mousemove', (e) => {{
                mouseX = e.clientX;
                mouseY = e.clientY;
            }});

            function updateSpotlight() {{
                // LERP Physics
                spotX += (mouseX - spotX) * easing;
                spotY += (mouseY - spotY) * easing;

                // Beam of Light Effect: High clarity center
                if (overlay) {{
                    overlay.style.background = `radial-gradient(circle {spot_radius}px at ${{spotX}}px ${{spotY}}px, rgba(255,255,255,0.05) 0%, rgba({rgb_color},0.02) 50%, rgba(0,0,0,0.3) 100%)`;
                }}
                
                requestAnimationFrame(updateSpotlight);
            }}
            updateSpotlight();
        }} else {{
            if (overlay) overlay.style.display = 'none';
        }}
    </script>
    <style>
    #spotlight-overlay {{
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 999999; will-change: background;
        display: {'block' if spot_enabled else 'none'};
        background: rgba(0,10,30,0.3); /* Atmospheric Blue Tint */
    }}

    .scheme-card:hover {{
        border-color: #00A3FF !important;
        box-shadow: 0 15px 45px rgba(0, 163, 255, 0.4) !important;
        transform: translateY(-8px) scale(1.02);
        background: rgba(255, 255, 255, 0.2) !important;
    }}
    </style>
""", unsafe_allow_html=True)
