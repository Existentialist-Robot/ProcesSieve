# frontend.py
import os
from nicegui import ui
from .main import app as fastapi_app
from .state import AppState

# Initialize state
state = AppState(
    # Get the absolute path to the service-account.json file
    service_account_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'service-account.json')),
    scopes=['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
)

@ui.page('/')
def show():
    mode = ui.dark_mode()
    with ui.header(elevated=True):
        ui.label("ProcesSieve Demo - Bagel Hacks Spring 2025")

    with ui.column().classes('w-full p-4'):
        ui.label("Dashboard Functions")

        # Input for Google Drive folder URL
        folder_url_input = ui.input(label="Google Drive Shared Folder URL", placeholder="Enter folder URL").classes('w-full')
        set_folder_button = ui.button("Set Folder URL", on_click=lambda: on_set_folder_url(folder_url_input.value))
        
        # Stage buttons
        def on_stage_change(stage: str):
            stage_index = state.stages.index(stage)
            state.set_stage(stage_index)

        state.create_stage_buttons(on_stage_change)

        prompt = (
                ui.textarea(
                    label="Input Prompt",
                    placeholder="start typing",
                    on_change=lambda e: result.set_text("you typed: " + e.value),
                )
                .props("clearable")
                .style("width: 50%; border: 2px")
            )
        result = ui.label().bind_text_from(prompt, "value")


        # Buttons to create documents and spreadsheets
        create_doc_button = ui.button("Create Document", on_click=lambda: state.create_document(
            title="My Programmatically Created Document",
            text="Hello world! This text was added via the Google Docs API using Python 🚀",
            share_email="eden@neuralberta.tech"
        ))

        create_sheet_button = ui.button("Create Spreadsheet", on_click=lambda: state.create_spreadsheet(
            title="My Programmatically Created Spreadsheet",
            data=[["Name", "Age", "Occupation"], ["Eden", "25", "AI Researcher"]],
            share_email="eden@neuralberta.tech"
        ))

    with ui.footer().style("background-color: #000000"):
        ui.label("Marc-Antoine, Eden, Dave")
    mode.enable()

def on_set_folder_url(folder_url: str):
    """Handle setting the folder URL and checking access."""
    state.set_folder_url(folder_url)
    state.drive_handler.check_folder_access()  # Add this line to check folder access after setting the URL

ui.run_with(
    fastapi_app,
    mount_path='/',
    storage_secret='pick your private secret here',
)
