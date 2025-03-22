from nicegui import ui


def main():
    print("Hello from ProcesSieve!")
    mode = ui.dark_mode()
    with ui.header(elevated=True):
        ui.label("ProcesSieve Demo - Bagle Hacks Spring 2025")
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

    with ui.footer().style("background-color: #000000"):
        ui.label("Marc-Antoine, Eden, Dave")
    mode.enable()
    ui.run()


if __name__ in {"__main__", "__mp_main__"}:
    main()
