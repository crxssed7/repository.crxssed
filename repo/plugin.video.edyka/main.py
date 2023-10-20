"""
edyka
"""
import sys

# pylint: disable=import-error
import xbmcgui
import xbmcplugin
# pylint: enable=import-error

from resources.lib.extractor import search_movie, search_tv, get_links

if sys.version_info >= (3,0,0):
    from urllib.parse import urlencode, parse_qsl
else:
    from urllib import urlencode
    from urlparse import parse_qsl

URL = sys.argv[0]
HANDLE = int(sys.argv[1])

def _build_url(**kwargs):
    """
    Creates a URL for the addon, e.g.
    plugin://plugin.video.edyka/mode=searchtv
    """
    return URL + "?" + urlencode(kwargs)

def list_searchables():
    """
    Addon entry point. Displays 'Movie' and 'TV' buttons
    """
    xbmcplugin.setPluginCategory(HANDLE, "edyka")
    xbmcplugin.setContent(HANDLE, "videos")

    movie_item = xbmcgui.ListItem(label="Movies")
    movie_item.setInfo("video", {
        "title": "Movies",
        "mediatype": "video"
    })
    url = _build_url(mode="searchmovie")
    xbmcplugin.addDirectoryItem(HANDLE, url, movie_item, True)

    tv_item = xbmcgui.ListItem(label="TV")
    tv_item.setInfo("video", {
        "title": "TV",
        "mediatype": "video"
    })
    url = _build_url(mode="searchtv")
    xbmcplugin.addDirectoryItem(HANDLE, url, tv_item, True)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_SIZE)
    xbmcplugin.endOfDirectory(HANDLE)

def _listing(edy_items):
    """
    Creates a virtual Kodi directory with list items
    """
    xbmcplugin.setPluginCategory(HANDLE, "edyka - listing")
    xbmcplugin.setContent(HANDLE, "videos")
    for link in edy_items:
        list_item = xbmcgui.ListItem(label=link["title"])
        title = link["title"]
        href = link["href"]
        size = link["size"]
        playable = link["playable"]
        list_item.setInfo("video", {
            "title": title,
            "size": size,
            "mediatype": "video"
        })
        if playable:
            m = "play"
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
        else:
            m = "listing"
            is_folder = True
        url = _build_url(mode=m, source=href)
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)

def list_movies(query):
    """
    Searches for movies with given query and displays them in a Kodi directory
    """
    results = search_movie(query)
    _listing(results)

def list_tv(query):
    """
    Searches for shows with given query and displays them in a Kodi directory
    """
    results = search_tv(query)
    _listing(results)

def list_links(source):
    """
    Displays a list of entries based on what is returned from an edy URL
    """
    links = get_links(source)
    _listing(links)

def play(source):
    """
    Plays a video from a URL
    """
    play_item = xbmcgui.ListItem(path=source)
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)

def validate_source(source):
    """
    Checks if the given source is valid or not
    """
    if not source:
        raise ValueError("You must provide a source")

    if not source.startswith("https://edytjedhgmdhm.abfhaqrhbnf.workers.dev"):
        raise ValueError("Source must be for edytjedhgmdhm")

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    """
    params = dict(parse_qsl(paramstring))

    if not params:
        list_searchables()
    else:
        mode = params.get("mode", None)
        source = params.get("source", None)
        if mode == "searchmovie":
            query = xbmcgui.Dialog().input('Search movie...', type=xbmcgui.INPUT_ALPHANUM)
            if query:
                list_movies(query)
            else:
                quit()
        elif mode == "searchtv":
            query = xbmcgui.Dialog().input('Search tv...', type=xbmcgui.INPUT_ALPHANUM)
            if query:
                list_tv(query)
            else:
                quit()
        elif mode == "listing":
            validate_source(source)
            list_links(source)
        elif mode == "play":
            validate_source(source)
            play(source)

if __name__ == '__main__':
    router(sys.argv[2][1:])
