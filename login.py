from nicegui import ui
import sessioncontroller
from internationalization import translate


@ui.page('/login')
async def loginPage():
    if sessioncontroller.hasToken():
        ui.navigate.to('/app')

    else:
        ui.label(translate('loginHeader'))
        ui.input(label=translate('loginServerIP'), placeholder='https://server.example.com:8096/jellyfin',
                 value=sessioncontroller.serverIp).bind_value(LoginHelper, 'server')
        ui.input(label=translate('loginUsername'), placeholder='user').bind_value(LoginHelper, 'user')
        ui.input(label=translate('loginPassword'), password=True, password_toggle_button=True).bind_value(LoginHelper, 'pw')
        ui.button(text=translate('loginLoginButton'), on_click=LoginHelper.loginHelper)


class LoginHelper:
    pw = ''
    user = ''
    server = ''

    def __init__(self):
        pass

    async def loginHelper(self):
        res = await sessioncontroller.loginUsername(LoginHelper.server, LoginHelper.user, LoginHelper.pw)
        match res:
            case 'Success':
                pass
            case 'BadCredentials':
                ui.notify(translate('loginErrorWrongLogin'))
            case 'InvalidUrl':
                ui.notify(translate('loginErrorInvalidUrl'))
            case _:
                ui.notify(translate('GeneralErrorUnknown'))


