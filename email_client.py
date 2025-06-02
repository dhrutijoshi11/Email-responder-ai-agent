from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.modify"])
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_unread_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD']).execute()
    messages = results.get('messages', [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        # parse payload, headers to extract subject, body etc.
        # mark as read after processing
        emails.append(msg_data)
    return emails

def send_email(to, subject, body):
    # Compose MIME message and send via Gmail API
    pass
