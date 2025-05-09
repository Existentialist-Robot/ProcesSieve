# drive.py
import re
from urllib.parse import parse_qs, urlparse

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Note on scopes: see https://developers.google.com/identity/protocols/oauth2/scopes#drive


class GoogleDriveHandler:
    def __init__(
        self,
        service_account_file,
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    ):
        self.service_account_file = service_account_file
        self.scopes = scopes
        self._authenticate()

    def _authenticate(self):
        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes
        )
        self.drive_service = build("drive", "v3", credentials=self.credentials)
        self.docs_service = build("docs", "v1", credentials=self.credentials)
        self.sheets_service = build("sheets", "v4", credentials=self.credentials)

    def set_folder_from_url(self, folder_url: str):
        """Extract folder ID from shared Google Drive folder URL."""
        folder_id_match = re.search(r"/folders/([a-zA-Z0-9_-]+)", folder_url)
        if folder_id_match:
            self.folder_id = folder_id_match.group(1)
            print(f"✅ Folder ID extracted (regex): {self.folder_id}")

        else:
            parsed_url = urlparse(folder_url)
            query_params = parse_qs(parsed_url.query)
            folder_id = query_params.get("id", [None])[0]
            if not folder_id:
                raise ValueError(
                    "Invalid Google Drive folder URL. Ensure it is a shared folder link."
                )

            self.folder_id = folder_id
            print(f"✅ Folder ID extracted (query param): {self.folder_id}")

        try:
            r = (
                self.drive_service.files()
                .get(fileId=self.folder_id, supportsAllDrives=True)
                .execute()
            )
            print(r)
            self.drive_id = r["driveId"]
        except:
            print("Could not get the driveId")
            raise

    def create_document(self, title: str, text: str, share_email: str = None):
        """Create a Google Doc in the specified folder and insert text."""
        if not hasattr(self, "folder_id"):
            raise ValueError("Folder ID not set. Call set_folder_from_url first.")

        print(f"Using folder ID: {self.folder_id}")  # Debug log
        file_metadata = {
            "name": title,
            "parents": [self.folder_id],
            "mimeType": "application/vnd.google-apps.document",
            "teamDriveId": self.drive_id,
        }

        print(file_metadata)

        try:
            doc = (
                self.drive_service.files()
                .create(body=file_metadata, supportsAllDrives=True)
                .execute()
            )
            doc_id = doc.get("id")
            print(f"✅ Document created: {title} (ID: {doc_id})")
        except HttpError as e:
            print(f"❌ Error creating document: {e}")
            raise

        try:
            insert_text_request = {
                "requests": [{"insertText": {"location": {"index": 1}, "text": text}}]
            }
            self.docs_service.documents().batchUpdate(
                documentId=doc_id, body=insert_text_request
            ).execute()
            print(f"✍️ Text inserted into the document.")
        except HttpError as e:
            print(f"❌ Error inserting text into document: {e}")
            raise

        if share_email:
            try:
                self._share_file(doc_id, share_email)
            except HttpError as e:
                print(f"❌ Error sharing document: {e}")
                raise

        return f"https://docs.google.com/document/d/{doc_id}/edit"

    def create_spreadsheet(self, title: str, data: list, share_email: str = None):
        """Create a Google Sheet in the specified folder and populate with data."""
        if not hasattr(self, "folder_id"):
            raise ValueError("Folder ID not set. Call set_folder_from_url first.")

        print(f"Using folder ID: {self.folder_id}")  # Debug log
        spreadsheet = {
            "properties": {"title": title, "parents": [{"id": self.folder_id}]},
            "sheets": [{"properties": {"sheetType": "GRID", "title": "Sheet1"}}],
        }

        try:
            spreadsheet = (
                self.sheets_service.spreadsheets().create(body=spreadsheet).execute()
            )
            spreadsheet_id = spreadsheet.get("spreadsheetId")
            print(f"✅ Spreadsheet created: {title} (ID: {spreadsheet_id})")
        except HttpError as e:
            print(f"❌ Error creating spreadsheet: {e}")
            raise

        if data:
            try:
                self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range="Sheet1!A1",
                    valueInputOption="RAW",
                    body={"values": data},
                ).execute()
                print(f"✍️ Data inserted into the spreadsheet.")
            except HttpError as e:
                print(f"❌ Error inserting data into spreadsheet: {e}")
                raise

        if share_email:
            try:
                self._share_file(spreadsheet_id, share_email)
            except HttpError as e:
                print(f"❌ Error sharing spreadsheet: {e}")
                raise

        return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    def check_folder_access(self):
        """Check if the folder is accessible by listing its contents."""
        try:
            files = (
                self.drive_service.files()
                .list(
                    q=f"'{self.folder_id}' in parents and trashed = false",
                    spaces="drive",
                    fields="files(id, name, permissions)",
                    includeTeamDriveItems=True,
                    supportsAllDrives=True,
                    pageSize=10,
                )
                .execute()
            )
            print(f"✅ Folder accessible. Files in folder: {files.get('files', [])}")

            for file in files.get("files", []):
                permissions = file.get("permissions", [])
                has_access = any(
                    perm["emailAddress"] == self.service_account_email
                    for perm in permissions
                )
                print(f"File: {file['name']}, Service Account has access: {has_access}")

        except HttpError as e:
            print(f"❌ Error accessing folder: {e}")
            raise

    def _share_file(self, file_id: str, email: str):
        """Share a file with the specified email address."""
        permission = {"type": "user", "role": "writer", "emailAddress": email}
        try:
            self.drive_service.permissions().create(
                fileId=file_id, body=permission, fields="id"
            ).execute()
            print(f"📤 File shared with: {email}")
        except HttpError as e:
            print(f"❌ Error sharing file: {e}")
            raise
