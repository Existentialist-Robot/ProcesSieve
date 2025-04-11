"""
High level programs that will start on set conditions and stops/shifts on others

1. Organization Stand-up What are you passionate about, what gaps do you see in the ecosystem

    Goal: Understand user passions and ecosystem gaps.
    Chatbot Flow:
        Ask: "What are you passionate about? What gaps do you see in your ecosystem?"
        Capture responses and store them as foundational data for the program.
        Example:
        User: "I’m passionate about sustainable agriculture, and I see a gap in education for small farmers."
        Chatbot: "Great! Let’s build a program to address that. Next, we’ll define high-level constraints and structure."

2. Program Stand-up *high level constraints (costs/people & bandwidth) + Overview + SOPs "We just created the bones of your new Program would you like to create an instantiation of this Program?" Create a project management sheet Create a sheet that follows a standard KPI format in each case/program drive (there will only be two) - that maps directly onto the database schema - the evaluation for a given

    Goal: Define high-level constraints, overview, and SOPs, roles and responsibilities based on # of people.
    Chatbot Flow:
        Ask: "What are your constraints (e.g., budget, team bandwidth) for this program?"
        Provide a template for the program overview and SOPs.
        Prompt: "We’ve created the bones of your program. Would you like to create an instantiation?"
        If "Yes":
        Generate a project management sheet (e.g., Google Sheets or Airtable) with placeholders for tasks, timelines, and responsibilities.
        Create a KPI sheet mapped to the database schema (e.g., columns for metrics, targets, and actuals).
        Example:
        Chatbot: "Your program overview is ready. Here’s a draft SOP. Shall we proceed to instantiation?"

3. Program Instantiation Set specific KPIs (right now we have a single imutable high level)

    Goal: Set specific KPIs and finalize the program structure, including a project management sheet.
    Chatbot Flow:
        Ask: "What specific KPIs would you like to track for this program?"
        Guide the user to define measurable, time-bound KPIs.
        Update the KPI sheet and database schema accordingly.
        Example:
        User: "I want to track the number of farmers trained and their yield increase."
        Chatbot: "Got it! I’ve updated your KPI sheet and database schema. Ready to launch?"

4. Program Eval (noticed you don't have any programs - would you like to co-create some?) Change in the constrains? Ask for eval/general feedback/specific changes to Overview/SOPs - post-event, based on:
    Group post-mortem minutes Individual feedback from internal (admin) and external (participants) Accept any suggested changes - create an new Case Template schema and now this is what the Case now points to

    Goal: Gather feedback, evaluate changes, and update the program.
    Chatbot Flow:
        Check if programs exist; if not, prompt: "Noticed you don’t have any programs. Would you like to co-create some?"
        If programs exist:
        Ask: "Have there been changes in constraints? How would you evaluate this program?"
        Collect feedback from post-mortem minutes, internal, and external sources.
        Prompt: "Would you like to accept suggested changes and update the Case Template schema?"
        If "Yes":
        Update the database schema and KPI sheet to reflect changes.
        Example:
        Chatbot: "Based on feedback, we’ve updated the SOPs and KPIs. Here’s the new Case Template schema."
"""

# state.py
from .drive import GoogleDriveHandler
from nicegui import ui


class AppState:
    def __init__(self, service_account_file, scopes):
        self.drive_handler = GoogleDriveHandler(service_account_file, scopes)
        self.folder_url = None
        self.stages = [
            "Organization",
            "Program Stand-up",
            "Program Instantiation",
            "Program Evaluation",
        ]
        self.stage_prompts = [
            "",
            "",
            "",
            "",
        ]
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
            ui.notify(
                f"Spreadsheet created successfully! URL: {sheet_url}", type="positive"
            )
        except Exception as e:
            ui.notify(f"Error creating spreadsheet: {str(e)}", type="negative")

    def _update_button_states(self):
        """Enable/disable buttons based on the current stage."""
        for i, button in enumerate(self.buttons):
            if i <= self.current_stage_index:
                button.props(remove="disabled")
            else:
                button.props("disabled")

    def set_stage(self, stage_index: int):
        """Set the current stage and update button states."""
        if 0 <= stage_index < len(self.stages):
            self.current_stage_index = stage_index
            self._update_button_states()
            ui.notify(f"Moved to stage: {self.stages[stage_index]}")

    def create_stage_buttons(self, on_stage_change):
        """Create buttons for each stage and link them to stage transitions."""
        with ui.row().classes("flex flex-wrap gap-2"):
            for stage in self.stages:
                button = ui.button(
                    stage, on_click=lambda stage=stage: on_stage_change(stage)
                )
                button.props("disabled outline")
                self.buttons.append(button)
        self._update_button_states()
