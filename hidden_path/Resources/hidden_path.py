import asyncio
import json
import re
from urllib.parse import urljoin, urldefrag

import aiohttp


LINK_RE = re.compile(r'<a\s+href="([^"]+)"', re.IGNORECASE)


def extract_links(html: str) -> list[str]:
    return LINK_RE.findall(html)


async def fetch_text(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()


async def crawl_readmes(
    base_url: str,
    *,
    concurrency: int = 20,
    timeout_s: int = 15,
) -> list[tuple[str, str]]:
    """
    Возвращает список (url_файла_README, содержимое).
    base_url — стартовая страница/директория (например, https://example.com/path/)
    """
    timeout = aiohttp.ClientTimeout(total=timeout_s)
    connector = aiohttp.TCPConnector(limit_per_host=concurrency)

    sem = asyncio.Semaphore(concurrency)
    queue: asyncio.Queue[str] = asyncio.Queue()
    visited: set[str] = set()

    await queue.put(base_url)
    visited.add(base_url)

    readmes: list[tuple[str, str]] = []

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:

        async def worker() -> None:
            while True:
                url = await queue.get()
                try:
                    async with sem:
                        html = await fetch_text(session, url)

                    for href in extract_links(html):
                        if href in ("../", "./"):
                            continue

                        # Склеиваем ссылки правильно
                        abs_url = urljoin(url, href)
                        abs_url, _ = urldefrag(abs_url)  # убрать #якоря

                        if abs_url in visited:
                            continue
                        visited.add(abs_url)

                        # Если это README — читаем как текст
                        if href.rstrip("/").upper() == "README":
                            async with sem:
                                content = await fetch_text(session, abs_url)
                            readmes.append((abs_url, content))
                        else:
                            # Иначе добавляем в очередь на дальнейший обход
                            await queue.put(abs_url)

                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    # В реальном коде можно логировать
                    # print(f"Skip {url}: {e}")
                    pass
                finally:
                    queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(concurrency)]

        await queue.join()
        for w in workers:
            w.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

    return readmes


async def main():
    base = "http://192.168.122.213" + "/.hidden/"
    readmes = await crawl_readmes(base, concurrency=20)

    print(f"Found README files: {len(readmes)}")
    with open("readme.json", "w+") as f:
        json.dump(readmes, f, ensure_ascii=False, indent=2)
    for url, content in readmes[:5]:
        print("=" * 60)
        print(url)
        print(content[:400])


if __name__ == "__main__":
    asyncio.run(main())

