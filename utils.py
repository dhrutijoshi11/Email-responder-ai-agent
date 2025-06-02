import re
from email.message import EmailMessage

def extract_email_body(payload: dict) -> str:
    """
    Extracts and decodes the plain text body from Gmail payload.
    """
    try:
        parts = payload['payload'].get('parts', [])
        for part in parts:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data', '')
                return decode_base64(data)
    except Exception:
        return payload.get("snippet", "")
    return ""

def decode_base64(data: str) -> str:
    import base64
    try:
        decoded_bytes = base64.urlsafe_b64decode(data + '==')
        return decoded_bytes.decode("utf-8")
    except Exception:
        return "[Unable to decode]"

def clean_email_text(text: str) -> str:
    """
    Clean up line breaks, excessive whitespace, etc.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def format_response_for_email(reply: str) -> str:
    """
    Optionally wrap or format response before sending.
    """
    return f"Dear Customer,\n\n{reply}\n\nBest regards,\nSupport Team"
