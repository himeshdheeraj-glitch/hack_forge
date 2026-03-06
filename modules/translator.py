from deep_translator import GoogleTranslator

def translate_text(text, target_lang='hi'):
    """
    Translates text to the target language.
    target_lang: 'hi' for Hindi, 'te' for Telugu, 'en' for English
    """
    if not text:
        return ""
        
    try:
        # GoogleTranslator is free and doesn't require an API key in this library's implementation
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return text # Return original text on failure
