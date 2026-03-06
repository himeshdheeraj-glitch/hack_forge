# 🏛️ AI Policy Navigator for Public Benefits

An AI-powered system to help citizens understand government policies, discover schemes, and determine eligibility using local, private, and free AI technologies.

## 🌟 Overview
Government policies are often written in complex legal language and spread across numerous documents, making them inaccessible to the average citizen. **AI Policy Navigator** bridges this gap using Retrieval Augmented Generation (RAG) and Speech-to-Text technologies to create a conversational, multilingual, and social-impact-focused assistant.

## 🚀 Features
1.  **AI Policy Chatbot**: Conversational RAG-based AI that answers questions based on uploaded PDFs.
2.  **Voice Assistant**: Accessibility for rural users via Speech-to-Text and Text-to-Speech.
3.  **Scheme Recommendation Engine**: rule-based discovery of benefits based on user profile.
4.  **Multilingual Support**: Real-time translation (English/Hindi) using `deep-translator`.
5.  **Policy Simplifier**: Converts complex legal jargon into simple human language.
6.  **Comparison Engine**: Side-by-side analysis of different government schemes.
7.  **Fraud & Fake Scheme Detector**: Checks suspicious messages against official policy records.
8.  **Eligibility Simulator**: Allows users to see how changes in income or age affect their benefits.
9.  **Analytics Dashboard**: Visualizes search trends and policy load metrics.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **LLM/Embeddings**: HuggingFace Transformers (Local)
- **Vector DB**: FAISS
- **Pipeline**: LangChain
- **Voice**: SpeechRecognition, pyttsx3
- **Translation**: deep-translator
- **Data**: pypdf, plotly

## 🏗️ Architecture
The system uses a **Retrieval Augmented Generation (RAG)** pipeline:
1.  **PDF Ingestion**: Policies are converted to text and split into chunks.
2.  **Vectorization**: `sentence-transformers` creates embeddings stored in `FAISS`.
3.  **Retrieval**: User queries search the vector store for the most relevant context.
4.  **Generation**: A local LLM (`google/flan-t5-base`) generates a grounded answer.

## 💻 Installation & Setup
1.  **Clone the directory**:
    ```bash
    cd hackforge
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Install System Dependencies (for voice)**:
    - macOS: `brew install portaudio`
    - Linux: `sudo apt-get install python3-pyaudio`

## 🏃 Project Execution
```bash
streamlit run app.py
```

## 📝 Hackathon Demo Workflow
1.  **Upload Samples**: Upload the provided sample PDFs in the sidebar.
2.  **Ask AI**: Ask "Who is eligible for PM Kisan scheme?".
3.  **Check Sources**: Show the document names and confidence scores.
4.  **Switch Language**: Change the language to Hindi and see the answers translate.
5.  **Voice Interaction**: Click the microphone and ask about healthcare benefits.
6.  **Discovery**: Fill the eligibility form to see recommended schemes for a farmer.
7.  **Fraud Check**: Paste a "free gift" message into the Fraud Detector.

## 🛡️ Trust and Transparency
- All answers include **Source Citations**.
- **Confidence Scores** are displayed for every AI response.
- Runs **100% Locally** (Privacy & Security for sensitive citizen data).

---
Built with ❤️ for social impact.
