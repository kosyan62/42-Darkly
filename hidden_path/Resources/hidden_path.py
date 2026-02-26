import asyncio
import os
import re
from urllib.parse import urljoin, urldefrag

import aiohttp

LINK_RE = re.compile(r'<a\s+href="([^"]+)"', re.IGNORECASE)
FLAG_RE = re.compile(r"[a-f0-9]{64}")


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
    timeout_s: int = 30,
) -> list[tuple[str, str]]:
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
                        abs_url = urljoin(url, href)
                        abs_url, _ = urldefrag(abs_url)
                        if abs_url in visited:
                            continue
                        visited.add(abs_url)

                        if href.rstrip("/").upper() == "README":
                            async with sem:
                                content = await fetch_text(session, abs_url)
                            readmes.append((abs_url, content))
                        else:
                            await queue.put(abs_url)

                except (aiohttp.ClientError, asyncio.TimeoutError):
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
    VM_IP = os.environ.get("VM_IP")
    if not VM_IP:
        raise SystemExit("Error: VM_IP environment variable is not set. Usage: VM_IP=<ip> python hidden_path.py")
    base = f"http://{VM_IP}/.hidden/"
    print(f"Crawling {base} ...")

    readmes = await crawl_readmes(base, concurrency=20)
    print(f"Scanned {len(readmes)} README files")

    for url, content in readmes:
        match = FLAG_RE.search(content)
        if match:
            print(f"Flag: {match.group()}")
            print(f"URL:  {url}")
            return

    print("Flag not found")


if __name__ == "__main__":
    asyncio.run(main())
