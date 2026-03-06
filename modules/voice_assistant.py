import threading
import io

def browser_stt_html(lang_code='en', return_tab=None):
    """Generates a high-end web-native STT interface with absolute top-level link redirection."""
    lang_map = {'en': 'en-IN', 'hi': 'hi-IN', 'te': 'te-IN'}
    target_lang = lang_map.get(lang_code, 'en-IN')
    
    html_code = f"""
        <div style="text-align:center; font-family:'Public Sans', sans-serif;">
            <button id="micBtn" style="
                background: linear-gradient(135deg, #004080, #00264d);
                color: white; border: none; padding: 20px 45px;
                border-radius: 50px; font-size: 1.3rem; cursor: pointer;
                box-shadow: 0 4px 25px rgba(0,0,0,0.3); transition: all 0.3s ease;
                display: flex; align-items: center; justify-content: center; margin: 0 auto;
                font-weight: bold;
            ">
                <span id="micIcon" style="font-size: 2rem; margin-right: 15px;">🎤</span>
                <span id="micText">Tap to Speak</span>
            </button>
            <p id="status" style="margin-top: 20px; color: #555; font-size: 1rem; font-weight: 500;">
                Click the microphone and ask your policy question.
            </p>
            
            <div id="resultBox" style="
                margin-top: 30px; padding: 30px; background: #ffffff;
                border-radius: 15px; border: 3px solid #004080; display:none;
                box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            ">
                <p style="color:#004080; font-weight:bold; margin:0 0 12px 0; font-size:1rem; text-transform:uppercase; letter-spacing:1px;">Question Captured:</p>
                <div id="transcript" style="font-size:1.5rem; color:#111; font-weight:700; margin-bottom:25px; line-height:1.4;"></div>
                
                <a id="searchLink" target="_top" style="
                    display: block; padding: 20px; background: #d93025; 
                    color: white !important; text-decoration: none !important; border-radius: 12px;
                    font-weight: 800; font-size: 1.3rem;
                    box-shadow: 0 6px 20px rgba(217,48,37,0.4);
                    text-align: center; border: none; outline: none;
                ">🔍 FIND ANSWER IN DOCUMENT</a>
                
                <p style="color:#28a745; font-size:1rem; margin-top:20px; font-weight:bold;">
                    Searching document... Click the RED button if it stops.
                </p>
            </div>
        </div>

        <script>
            const micBtn = document.getElementById('micBtn');
            const micText = document.getElementById('micText');
            const micIcon = document.getElementById('micIcon');
            const status = document.getElementById('status');
            const resultBox = document.getElementById('resultBox');
            const transcriptArea = document.getElementById('transcript');
            const searchLink = document.getElementById('searchLink');

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

            if (SpeechRecognition) {{
                const recognition = new SpeechRecognition();
                recognition.lang = '{target_lang}';
                recognition.continuous = false;
                recognition.interimResults = false;

                recognition.onstart = () => {{
                    micBtn.style.background = "#d93025";
                    micText.innerText = "Listening...";
                    micIcon.innerText = "⏹️";
                    status.innerText = "Please speak clearly into your mic...";
                    status.style.color = "#d93025";
                }};

                recognition.onresult = (event) => {{
                    const text = event.results[0][0].transcript;
                    transcriptArea.innerText = '"' + text + '"';
                    resultBox.style.display = "block";
                    micBtn.style.display = "none";
                    status.innerText = "Captured! Processing query...";
                    
                    const params = new URLSearchParams({{
                        voice_query: text,
                        tab: "{return_tab if return_tab is not None else "0"}"
                    }});
                    const finalUrl = window.top.location.origin + window.top.location.pathname + "?" + params.toString();
                    searchLink.href = finalUrl;
                    
                    // Automatic redirection attempt
                    setTimeout(() => {{
                        try {{
                            window.top.location.href = finalUrl;
                        }} catch(e) {{
                            console.log("Top level redirect error, please click the button.");
                        }}
                    }}, 1500);
                }};

                recognition.onerror = (event) => {{
                    status.innerText = "Mic Error: " + event.error + ". Please enable microphone access.";
                    status.style.color = "red";
                    micBtn.style.background = "#004080";
                    micText.innerText = "Tap to Retry";
                }};

                micBtn.onclick = () => {{
                    try {{
                        recognition.start();
                    }} catch(e) {{
                        recognition.stop();
                    }}
                }};
            }} else {{
                status.innerText = "Voice features require Google Chrome.";
                micBtn.disabled = true;
                micBtn.style.opacity = "0.5";
            }}
        </script>
    """
    return html_code

def browser_speak(text, lang_code='en'):
    """Placeholder for backward compatibility. Audio is disabled."""
    return ""
