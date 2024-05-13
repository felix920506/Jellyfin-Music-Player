from sessioncontroller import requestMaker, serverIp
import aiohttp


async def getLibs():
    res = await requestMaker('GET', 'UserViews')
    reslist: list[dict] = []
    for item in res['Items']:
        if item['CollectionType'] in ['music']:
            entry = {
                'Id': item['Id'],
                'Name': item['Name'],
                'Image': getImageUrl(item['Id'])
            }
            reslist.append(entry)

    return reslist


async def getItemDetails(id: str) -> dict:
    res = await requestMaker('GET', f'Items/{id}')
    return res


async def getLibItems(id: str) -> list[dict]:
    res = await requestMaker('GET', 'Items', f'parentId={id}&recursive=true&includeItemTypes=MusicAlbum')
    return res['Items']


def getImageUrl(id: str) -> str:
    return f'{serverIp}/Items/{id}/Images/Primary/0'


async def getAlbumTracks(id: str) -> list[dict]:
    res = await requestMaker('GET', 'Items', f'parentId={id}')
    return res
