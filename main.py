from nicegui import ui
import login
import index


@ui.page('/')
def landingPage():
    ui.navigate.to('/login')


ui.run()
