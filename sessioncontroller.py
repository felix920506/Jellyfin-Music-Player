import aiohttp
import platform
import json


# TODO: Refactor to read from external file
VERSION = '0.0.1'
CLIENT = 'Jellyfin Music Player'
CLIENTID = '12345'

# Use device name as Jellyfin device name
DEVICE = platform.node()

# Load authentication info from previous session(s)
try:
    with open('./data/auth.json', 'r', encoding='utf8') as authFile:
        auth = json.load(authFile)

except:
    # Load file failed: blank token and IP, start over
    serverIp: str = ''
    _token: str = ''

else:
    # Use the items present to authenticate
    if 'serverIp' in auth:
        serverIp = auth['serverIp']

    if 'token' in auth:
        _token = auth['token']


async def loginUsername(server: str, username: str, password: str):
    async with aiohttp.ClientSession(headers=_buildHeader()) as session:
        body = {
            'Username': username,
            'Pw': password
        }
        try:
            async with session.post(f'{server}/Users/AuthenticateByName', json=body) as auth:
                global serverIp
                serverIp = server
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


async def loginQuickConnect(server: str, code: str):
    pass


def _buildHeader():
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
