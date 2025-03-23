from nicegui import ui
from .main import app as fastapi_app
from .state import ConversationState

@ui.page('/')
def show():
    mode = ui.dark_mode()
    with ui.header(elevated=True):
        ui.label("ProcesSieve Demo - Bagel Hacks Spring 2025")
    ui.label("Dashboard Functions")
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

    # Stage buttons
    def on_stage_change(stage: str):
        stage_index = state.stages.index(stage)
        state.set_stage(stage_index)

    state.create_stage_buttons(on_stage_change)

    with ui.footer().style("background-color: #000000"):
        ui.label("Marc-Antoine, Eden, Dave")
    mode.enable()

ui.run_with(
    fastapi_app,
    mount_path='/',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
    storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
)
