#!/usr/bin/env python3

import sys
import re
import time
from urllib.request import urlopen
from urllib.parse import quote, unquote
from urllib.error import URLError, HTTPError

WIKIPEDIA_BASE = "https://ru.wikipedia.org/wiki/"


def get_content(name):
    try:
        name = unquote(name)
        url = WIKIPEDIA_BASE + quote(name)
        print(f"Р—Р°РіСЂСѓР¶Р°РµРј: {url}")
        with urlopen(url) as response:
            return response.read().decode("utf-8", errors="ignore")
    except (URLError, HTTPError):
        print(f"РћС€РёР±РєР° Р·Р°РіСЂСѓР·РєРё!")
        return None


def extract_content(page):
    match = re.search(r'<div[^>]+id="mw-content-text"[^>]*>', page)
    if not match:
        return 0, 0

    start = match.end()

    end_match = re.search(r'<div class="printfooter">', page[start:])
    end = start + end_match.start() if end_match else len(page)

    return start, end


def extract_links(page, begin, end):
    content = page[begin:end]
    links = re.findall(r'<[aA]\s*[Hh]ref=["\']/wiki/([^"#\':]*)["\']', content)
    decoded_links = {unquote(link) for link in links}
    print(f"РќР°Р№РґРµРЅРѕ СЃСЃС‹Р»РѕРє: {len(decoded_links)}. РЎСЃС‹Р»РєРё: {decoded_links}")
    return decoded_links


def find_chain(start, finish):
    visited = set()
    queue = [(start, [start])]

    while queue:
        current, path = queue.pop(0)
        if current in visited:
            continue

        print(f"РџРѕСЃРµС‰Р°РµРј: {current}")
        visited.add(current)
        page = get_content(current)
        if not page:
            continue

        begin, end = extract_content(page)
        links = extract_links(page, begin, end)

        for link in links:
            if link == finish:
                return path + [finish]
            if link not in visited:
                queue.append((link, path + [link]))

    return None


def main():
    if len(sys.argv) != 2:
        print("РСЃРїРѕР»СЊР·РѕРІР°РЅРёРµ: script.py <РЅР°Р·РІР°РЅРёРµ_СЃС‚Р°С‚СЊРё>")
        return

    start_article = sys.argv[1]
    finish_article = "Философия"
    chain = find_chain(start_article, finish_article)

    if chain:
        print(" -> ".join(chain))


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time()-start)
