from nicegui import ui
import sessioncontroller
from internationalization import translate


@ui.page('/login')
async def loginpage():
    if sessioncontroller.hasToken():
        ui.navigate.to('/index')

    else:
        ui.label(translate('loginHeader'))
        ui.input(label=translate('loginServerIP'), placeholder='https://server.example.com:8096/jellyfin').bind_value(LoginHelper, 'server')
        ui.input(label=translate('loginUsername'), placeholder='user').bind_value(LoginHelper, 'user')
        ui.input(label=translate('loginPassword'), password=True, password_toggle_button=True).bind_value(LoginHelper, 'pw')
        ui.button(text=translate('loginLoginButton'), on_click=LoginHelper.loginhelper)

class LoginHelper:
    pw = ''
    user = ''
    server = ''

    def __init__(self):
        pass

    async def loginhelper(self):
        res = await sessioncontroller.login(LoginHelper.server, LoginHelper.user, LoginHelper.pw)
        match res:
            case 'Success':
                pass
            case 'BadCredentials':
                ui.notify(translate('loginErrorWrongLogin'))
            case 'InvalidUrl':
                ui.notify(translate('loginErrorInvalidUrl'))
            case _:
                ui.notify(translate('loginErrorUnknown'))


