"""
extract from source
"""
import re
import requests

def _is_playable(href):
    playables = [".mkv", ".mp4", ".avi"]
    for formt in playables:
        if href.endswith(formt):
            return True
    return False

def get_links(url):
    response = requests.get(url)
    pattern = r'<tr class="file">.*?<a href="([^"]+)">([^<]+)</a>'
    matches = re.finditer(pattern=pattern, string=response.text, flags=re.DOTALL)
    links = []
    for m in matches:
        href = m.group(1)
        text = m.group(2)
        playable = _is_playable(href)

        links.append({"title": text, "href": url + href, "playable": playable})
    return links

def _search(url, query):
    available = get_links(url)
    results = []
    for tv in available:
        if query.lower() in tv["title"].lower():
            results.append(tv)
    return results

def search_tv(query):
    url = "https://edytjedhgmdhm.abfhaqrhbnf.workers.dev/tvs/"
    return _search(url, query)

def search_movie(query):
    url = "https://edytjedhgmdhm.abfhaqrhbnf.workers.dev/movies/"
    return _search(url, query)

# q = "wizards of Wav"
# results = search_tv(q)
# result = results[0] # simulate choice
# seasons = get_links(result["href"])
# season = seasons[0] # simulate choice
# episodes = get_links(season["href"])
# episode = episodes[0] # simulate choice
# print(episode)

# q = "The imitation game"
# results = search_movie(q)
# result = results[0]
# links = get_links(result["href"])
# movie = links[0]
# print(movie)
