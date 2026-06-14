"""Simple web scraper — fetches book listings from books.toscrape.com
(a sandbox site built for scraping practice) and saves them as JSON."""

import sys
import json
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import Optional
from urllib.parse import urljoin

BASE_URL = "http://books.toscrape.com/"


@dataclass
class Book:
    title: str
    price: str
    url: str
    in_stock: bool


def fetch(url: str) -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()  # raises on 4xx/5xx
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def parse_books(soup: BeautifulSoup, base_url: str) -> list[Book]:
    books = []
    for item in soup.select("article.product_pod"):
        link_el = item.select_one("h3 a")
        price_el = item.select_one("p.price_color")
        stock_el = item.select_one("p.instock.availability")

        if not (link_el and price_el):
            continue

        books.append(Book(
            title=link_el.get("title", "").strip(),
            price=price_el.get_text(strip=True),
            url=urljoin(base_url, link_el.get("href", "")),
            in_stock="In stock" in stock_el.get_text() if stock_el else False,
        ))
    return books


def save_report(items: list[Book], path: str = "report.json") -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(i) for i in items], f, indent=2, ensure_ascii=False)
    print(f"Saved {len(items)} items to {path}")


def main() -> None:
    url = sys.argv[1] if len(sys.argv) >= 2 else BASE_URL

    soup = fetch(url)
    if soup is None:
        sys.exit(1)

    books = parse_books(soup, url)
    if not books:
        print("No items found — check the CSS selectors against the page's HTML.")
        return

    for b in books[:5]:
        stock = "✓ in stock" if b.in_stock else "✗ out of stock"
        print(f"  {b.title:40.40} {b.price:>8}  {stock}")

    save_report(books)


if __name__ == "__main__":
    main()