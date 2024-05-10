import aiohttp
import platform
import json


# TODO: Refactor to read from external file
VERSION = '0.0.1'
CLIENT = 'Jellyfin Music Player'
CLIENTID = '12345'

DEVICE = platform.node()


try:
    with open('./data/auth.json', 'r', encoding='utf8') as authFile:
        auth = json.load(authFile)
        _serverIp = auth['serverIp']
        _token = auth['token']

except:
    _serverIp: str = ''
    _token: str = ''


async def login(server: str, username: str, password: str):
    async with aiohttp.ClientSession(headers=_buildheader()) as session:
        body = {
            'Username': username,
            'Pw': password
        }
        try:
            async with session.post(f'{server}/Users/AuthenticateByName', json=body) as auth:
                global _serverIp
                _serverIp = server
                if auth.status == 200:
                    body = json.loads(await auth.text())
                    global _token
                    _token = body['AccessToken']
                    with open('./data/auth.json', 'w', encoding='utf8') as authFile:
                        data = {
                            'serverIp': server,
                            'token': _token
                        }
                        json.dump(data, authFile)
                    return "Success"
                elif auth.status == 401:
                    return "BadCredentials"
                else:
                    return "UnknownError"
        except aiohttp.client_exceptions.InvalidURL:
            return "InvalidUrl"


async def loginquickconnect( server, code):
    pass


def _buildheader():
    headers = {
        "Authorization": f'MediaBrowser Client="{CLIENT}", Device="{DEVICE}", DeviceId="{CLIENTID}", Version="{VERSION}"'
    }
    if _token:
        headers["Authorization"] += f', Token="{_token}"'

    return headers


def hasToken():
    if _token:
        return True
    else:
        return False
