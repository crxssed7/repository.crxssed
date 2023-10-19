"""
vska - btw idk what half of this does :)
"""
import sys
from urllib.parse import parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

from resources.lib.vidsrc import movie, episode

URL = sys.argv[0]
HANDLE = int(sys.argv[1])
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))

def play_video(url):
    """
    huhu you'll never guess what this function does
    """
    item = xbmcgui.ListItem(offscreen=True)
    item.setPath(url)
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=item)

def play_movie(external_id):
    """
    Plays a movie... I think?
    """
    url = movie(external_id=external_id)
    if not url:
        raise ValueError("movie: URL is none")
    play_video(url)

def play_episode(external_id, season, episode_number):
    """
    god help me i can't decipher this python function
    """
    url = episode(external_id=external_id, season=season, episode_number=episode_number)
    if not url:
        raise ValueError("episode: URL is none")
    play_video(url)

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    """
    params = dict(parse_qsl(paramstring))
    external_id = params.get("id", None)
    season = params.get("season", None)
    episode_number = params.get("episode", None)
    if not external_id:
        raise ValueError("Missing external ID")

    if season and episode:
        play_episode(external_id=external_id, season=season, episode_number=episode_number)
    elif not season and not episode:
        play_movie(external_id=external_id)
    else:
        raise ValueError("You need to pass both season and episode or neither")


if __name__ == '__main__':
    router(sys.argv[2][1:])
