from nicegui import ui
from router import Router
from internationalization import translate
import mediacontroller


@ui.page('/app')
@ui.page('/app/{_:path}')
def appPage():
    router = Router()

    @router.add('/app')
    async def landingPage():
        ui.label(translate('LandingPageHeading'))
        libs = await mediacontroller.getLibs()
        print(libs)
        for lib in libs:
            with ui.card().tight().on('click', lambda libId = lib["Id"]: ui.navigate.to(f'/app/libs/{libId}')):
                ui.image(lib['Image'])
                ui.label(lib['Name'])

    @router.add('/app/libs/')
    async def libView():
        url = await ui.run_javascript('window.location.href')
        url = url.split('/')
        libId = url[5]
        try:
            page = int(url[6])
        except IndexError:
            page = 1
        libInfoReq = mediacontroller.getLibDetails(libId)
        libAlbumsReq = mediacontroller.getLibItems(libId)
        libInfo = await libInfoReq
        libAlbums = await libAlbumsReq
        ui.label(libInfo['Name'])
        for item in libAlbums:
            with ui.card().on('click', lambda: ui.navigate.to(f'/app/albums/{item["Id"]}')):
                ui.image(mediacontroller.getImageUrl(item['Id']))
                ui.label(item['Name'])
        pass


    @router.add('/app/albums/')
    async def albumView():
        url = await ui.run_javascript('window.location.href')
        url = url.split('/')
        albumId = url[5]
        ui.label(albumId)
        tracks = await mediacontroller.getAlbumTracks(albumId)
        print(tracks)

    # Places router contents on the page
    router.frame()

    ui.label('Player Goes Here')
