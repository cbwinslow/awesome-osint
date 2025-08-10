import sys
import yaml
import requests
from bs4 import BeautifulSoup
import webbrowser
from pathlib import Path

TOOLS_FILE = Path('tools.yaml')


def load_tools():
    if TOOLS_FILE.exists():
        with open(TOOLS_FILE) as f:
            return yaml.safe_load(f)
    return {}


def search_engine(engine_url, query):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = engine_url
    if "google" in engine_url:
        url = f"{engine_url}/search?q={query}"
    elif "duckduckgo" in engine_url:
        url = f"{engine_url}/?q={query}"
    elif "startpage" in engine_url:
        url = f"{engine_url}/do/search?q={query}"
    elif "dogpile" in engine_url:
        url = f"{engine_url}/search/web?q={query}"
    else:
        url = f"{engine_url}?q={query}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception:
        webbrowser.open(url)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        text = a.get_text(strip=True)
        if href.startswith("http") and text:
            results.append({"title": text, "url": href})
    return results


def aggregate(query):
    tools = load_tools()
    aggregated = []
    for group, items in tools.items():
        for tool in items:
            engine_results = search_engine(tool['url'], query)
            for res in engine_results:
                res['engine'] = tool['name']
                aggregated.append(res)
    dedup = {}
    for r in aggregated:
        dedup.setdefault(r['url'], r)
    return list(dedup.values())


def main():
    if len(sys.argv) < 2:
        print('Usage: python workflow.py "search query"')
        return
    query = "+".join(sys.argv[1:])
    results = aggregate(query)
    for r in results[:10]:
        print(f"[{r['engine']}] {r['title']} -> {r['url']}")


if __name__ == "__main__":
    main()
