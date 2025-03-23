from google.oauth2 import service_account
from googleapiclient.discovery import build

# ----------- CONFIGURATION -----------
SERVICE_ACCOUNT_FILE = '../service-account.json'  # 👈 Replace this with your actual path
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]
DOCUMENT_TITLE = 'My Programmatically Created Document'
TEXT_TO_INSERT = 'Hello world! This text was added via the Google Docs API using Python 🚀'
SHARE_WITH_EMAIL = 'eden@neuralberta.tech'  # 👈 Optional: Replace or remove if not needed
# --------------------------------------

# Authenticate with Google Docs & Drive APIs
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
docs_service = build('docs', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# Step 1: Create a new Google Doc
doc = docs_service.documents().create(body={'title': DOCUMENT_TITLE}).execute()
doc_id = doc.get('documentId')
print(f'✅ Document created: {DOCUMENT_TITLE} (ID: {doc_id})')

# Step 2: Insert content into the document
insert_text_request = [
    {
        'insertText': {
            'location': {'index': 1},
            'text': TEXT_TO_INSERT
        }
    }
]

docs_service.documents().batchUpdate(
    documentId=doc_id,
    body={'requests': insert_text_request}
).execute()
print(f'✍️ Text inserted into the document.')

# Step 3: (Optional) Share the document with someone
if SHARE_WITH_EMAIL:
    permission = {
        'type': 'user',
        'role': 'writer',  # 'reader' or 'writer'
        'emailAddress': SHARE_WITH_EMAIL
    }

    drive_service.permissions().create(
        fileId=doc_id,
        body=permission,
        fields='id'
    ).execute()
    print(f'📤 Document shared with: {SHARE_WITH_EMAIL}')

# Step 4: Print the document URL
print(f'📄 Document URL: https://docs.google.com/document/d/{doc_id}/edit')
