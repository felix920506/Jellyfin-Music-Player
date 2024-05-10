from nicegui import ui
import login
import app


@ui.page('/')
def landingPage():
    ui.navigate.to('/login')


ui.run()
