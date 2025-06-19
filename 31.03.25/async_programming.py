#!/usr/bin/env python3

import sys
import re
import asyncio
import time

import aiohttp
from urllib.parse import quote, unquote


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

WIKIPEDIA_BASE = "https://ru.wikipedia.org/wiki/"

async def get_content(name, session):
    try:
        name = unquote(name)
        url = WIKIPEDIA_BASE + quote(name)
        print(f"Загружаем: {url}")
        async with session.get(url) as response:
            # Передаём аргумент errors="ignore" для совместимости с исходным кодом
            return await response.text(errors="ignore")
    except Exception as e:
        print("Ошибка загрузки!")
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
    print(f"Найдено ссылок: {len(decoded_links)}. Ссылки: {decoded_links}")
    return decoded_links

async def find_chain(start, finish, session):
    visited = set()
    queue = [(start, [start])]

    while queue:
        current, path = queue.pop(0)
        if current in visited:
            continue

        print(f"Проходим: {current}")
        visited.add(current)
        page = await get_content(current, session)
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

async def main():
    if len(sys.argv) != 2:
        print("Использование: script.py <название_страницы>")
        return

    start_article = sys.argv[1]
    finish_article = "Философия"  # целевая статья
    async with aiohttp.ClientSession() as session:
        chain = await find_chain(start_article, finish_article, session)
        if chain:
            print(" -> ".join(chain))
        else:
            print("Цепочка не найдена.")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(time.time()-start)
