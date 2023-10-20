"""
edyka
"""
import sys
from urllib import urlencode
from urlparse import parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon

from resources.lib.extractor import search_movie, search_tv, get_links

URL = sys.argv[0]
HANDLE = int(sys.argv[1])

def build_url(**kwargs):
    return URL + "?" + urlencode(kwargs)

def list_searchables():
    """
    lists movie and tv list item
    """
    xbmcplugin.setPluginCategory(HANDLE, "edyka")
    xbmcplugin.setContent(HANDLE, "videos")

    movie_item = xbmcgui.ListItem(label="Movies")
    movie_item.setInfo("video", {
        "title": "Movies",
        "genre": "Movies",
        "mediatype": "video"
    })
    url = build_url(mode="searchmovie")
    xbmcplugin.addDirectoryItem(HANDLE, url, movie_item, True)

    tv_item = xbmcgui.ListItem(label="TV")
    tv_item.setInfo("video", {
        "title": "TV",
        "genre": "TV",
        "mediatype": "video"
    })
    url = build_url(mode="searchtv")
    xbmcplugin.addDirectoryItem(HANDLE, url, tv_item, True)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)

def list_movies(query):
    results = search_movie(query)
    xbmcplugin.setPluginCategory(HANDLE, "edyka - " + query)
    xbmcplugin.setContent(HANDLE, "videos")
    for result in results:
        list_item = xbmcgui.ListItem(label=result["title"])
        title = result["title"]
        list_item.setInfo("video", {
            "title": title,
            "genre": title,
            "mediatype": "video"
        })
        url = build_url(mode="listing")
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, True)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(HANDLE)

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    """
    params = dict(parse_qsl(paramstring))

    if not params:
        list_searchables()
    else:
        if params["mode"] == "searchmovie":
            query = xbmcgui.Dialog().input('Search movie...', type=xbmcgui.INPUT_ALPHANUM)
            if query:
                list_movies(query)
            else:
                quit()
        elif params["mode"] == "searchtv" or params["mode"] == "listing":
            raise NotImplementedError("Not implemented yet")


if __name__ == '__main__':
    router(sys.argv[2][1:])
