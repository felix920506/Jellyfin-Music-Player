from nicegui import ui


@ui.page('/app')
@ui.page('/app/{_:path}')
def indexPage():
    ui.label("Placeholder")