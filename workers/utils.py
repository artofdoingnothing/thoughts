import re

def remove_pii(text):
    if not text:
        return text
    # Email regex
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    # Phone regex (simple patterns)
    text = re.sub(r'(?<!\w)(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b', '[PHONE_REDACTED]', text)
    return text
