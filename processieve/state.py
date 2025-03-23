'''

High level programs that will start on set conditions and stops/shifts on others

1. Organization Stand-up 
	What are you passionate about, what gaps do you see in the ecosystem

2. Program Stand-up *high level constraints (costs/people & bandwidth) + Overview + SOPs
	"We just created the bones of your new Program would you like to create an instantiation of this Program?"
		Create a project management sheet
    Create a sheet that follows a standard KPI format in each case/program drive (there will only be two) - that maps directly onto the database schema - the evaluation for a given 

3. Program Instantiation 
        Set specific KPIs (right now we have a single imutable high level)

4. Program Eval (noticed you don't have any programs - would you like to co-create some?)
	Change in the constrains?	
    Ask for eval/general feedback/specific changes to Overview/SOPs - post-event, based on:
    - Group post-mortem minutes
    Individual feedback from internal (admin) and external (participants)
    	Accept any suggested changes - create an new Case Template schema and now this is what the Case now points to


'''# state.py
from typing import Callable
from nicegui import ui

class ConversationState:
    def __init__(self):
        self.stages = ["Organization", "Program Stand-up", "Program Instantiation", "Program Evaluation"]
        self.current_stage_index = -1  # Initially no stage is active
        self.buttons = []  # Store button references for UI updates

    def _update_button_states(self):
        """Enable/disable buttons based on the current stage."""
        for i, button in enumerate(self.buttons):
            if i <= self.current_stage_index:
                button.props(remove='disabled')  # Enable button
            else:
                button.props('disabled')  # Disable button

    def set_stage(self, stage_index: int):
        """Set the current stage and update button states."""
        if 0 <= stage_index < len(self.stages):
            self.current_stage_index = stage_index
            self._update_button_states()
            ui.notify(f"Moved to stage: {self.stages[stage_index]}")

    def next_stage(self):
        """Move to the next stage if available."""
        if self.current_stage_index < len(self.stages) - 1:
            self.set_stage(self.current_stage_index + 1)

    def get_current_stage(self) -> str:
        """Return the current stage name."""
        if self.current_stage_index >= 0:
            return self.stages[self.current_stage_index]
        return "No Stage Active"

    def create_stage_buttons(self, on_stage_change: Callable[[str], None]):
        """Create buttons for each stage and link them to stage transitions."""
        with ui.row():
            for stage in self.stages:
                button = ui.button(stage, on_click=lambda stage=stage: on_stage_change(stage))
                button.props('disabled outline')  # Start all buttons disabled
                self.buttons.append(button)
        self._update_button_states()

