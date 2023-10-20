"""
extract from source
"""
# pylint: disable=line-too-long
import sys
import re
import requests

if sys.version_info >= (3,0,0):
    import html
else:
    from HTMLParser import HTMLParser
    html = HTMLParser()

def _is_playable(href):
    playables = [".mkv", ".mp4", ".avi"]
    for formt in playables:
        if href.endswith(formt):
            return True
    return False

def _clamp(size):
    if size < 0:
        return 0
    return size

def get_links(url):
    """
    Get all the links from an edy directory
    """
    response = requests.get(url, timeout=60)
    pattern = r'<tr class="file">.*?<a href="([^"]+)">([^<]+)</a>.*?<td data-order="([^"]+)">.*?</tr>'
    matches = re.finditer(pattern=pattern, string=response.text, flags=re.DOTALL)
    links = []
    for m in matches:
        href = m.group(1)
        text = m.group(2)
        size = m.group(3)
        playable = _is_playable(href)

        links.append({"title": text, "href": html.unescape(url + href), "playable": playable, "size": _clamp(int(size))})
    return links

def _search(url, query):
    available = get_links(url)
    results = []
    for tv in available:
        if query.lower() in tv["title"].lower():
            results.append(tv)
    return results

def search_tv(query):
    """
    Searches for a TV show, returns a list of results
    """
    url = "https://edytjedhgmdhm.abfhaqrhbnf.workers.dev/tvs/"
    return _search(url, query)

def search_movie(query):
    """
    Searches for a movie, returns a list of results
    """
    url = "https://edytjedhgmdhm.abfhaqrhbnf.workers.dev/movies/"
    return _search(url, query)
