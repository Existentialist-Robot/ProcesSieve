# state.py
from .drive import GoogleDriveHandler
from nicegui import ui

class AppState:
    def __init__(self, service_account_file, scopes):
        self.drive_handler = GoogleDriveHandler(service_account_file, scopes)
        self.folder_url = None
        self.stages = ["Organization", "Program Stand-up", "Program Instantiation", "Program Evaluation"]
        self.current_stage_index = -1
        self.buttons = []

    def set_folder_url(self, folder_url: str):
        """Set the Google Drive folder URL and extract the folder ID."""
        self.folder_url = folder_url
        try:
            self.drive_handler.set_folder_from_url(folder_url)
            ui.notify("Folder URL set successfully!", type="positive")
        except ValueError as e:
            ui.notify(str(e), type="negative")

    def create_document(self, title: str, text: str, share_email: str = None):
        """Create a document in the specified folder."""
        if not self.folder_url:
            ui.notify("Please set a Google Drive folder URL first!", type="negative")
            return
        try:
            doc_url = self.drive_handler.create_document(title, text, share_email)
            ui.notify(f"Document created successfully! URL: {doc_url}", type="positive")
        except Exception as e:
            ui.notify(f"Error creating document: {str(e)}", type="negative")

    def create_spreadsheet(self, title: str, data: list, share_email: str = None):
        """Create a Google Sheet in the specified folder."""
        try:
            sheet_url = self.drive_handler.create_spreadsheet(title, data, share_email)
            ui.notify(f"Spreadsheet created successfully! URL: {sheet_url}", type="positive")
        except Exception as e:
            ui.notify(f"Error creating spreadsheet: {str(e)}", type="negative")

    def _update_button_states(self):
        """Enable/disable buttons based on the current stage."""
        for i, button in enumerate(self.buttons):
            if i <= self.current_stage_index:
                button.props(remove='disabled')
            else:
                button.props('disabled')

    def set_stage(self, stage_index: int):
        """Set the current stage and update button states."""
        if 0 <= stage_index < len(self.stages):
            self.current_stage_index = stage_index
            self._update_button_states()
            ui.notify(f"Moved to stage: {self.stages[stage_index]}")

    def create_stage_buttons(self, on_stage_change):
        """Create buttons for each stage and link them to stage transitions."""
        with ui.row().classes('flex flex-wrap gap-2'):
            for stage in self.stages:
                button = ui.button(stage, on_click=lambda stage=stage: on_stage_change(stage))
                button.props('disabled outline')
                self.buttons.append(button)
        self._update_button_states()
