import asyncio
import aiohttp
import pytest
from bs4 import BeautifulSoup
from collections import defaultdict
import csv

BASE_URL = "https://ru.wikipedia.org"
START_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"


async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_page(html):
    soup = BeautifulSoup(html, "lxml")
    counts = defaultdict(int)

    items = soup.select(".mw-category-group ul li a")
    for item in items:
        title = item.get_text(strip=True)
        if title:
            first_letter = title[0].upper()
            counts[first_letter] += 1

    next_link = soup.find("a", string="Следующая страница")
    next_url = BASE_URL + next_link["href"] if next_link else None

    return counts, next_url


async def get_animals_count_by_letter():
    url = START_URL
    all_counts = defaultdict(int)

    async with aiohttp.ClientSession() as session:
        while url:
            print(f"Парсинг: {url}")
            html = await fetch_html(session, url)
            counts, next_url = await parse_page(html)

            for letter, count in counts.items():
                all_counts[letter] += count

            url = next_url
            await asyncio.sleep(0.3)
    return all_counts


def save_to_csv(counts, filename="beasts.csv"):
    with open(filename, mode="w", encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])


async def main():
    counts = await get_animals_count_by_letter()
    save_to_csv(counts)
    print("Готово! Результаты сохранены в beasts.csv")

HTML_WITH_NEXT = """
<div class="mw-category">
  <div class="mw-category-group">
    <ul>
      <li><a href="/wiki/Акула">Акула</a></li>
      <li><a href="/wiki/Антилопа">Антилопа</a></li>
      <li><a href="/wiki/Бобр">Бобр</a></li>
    </ul>
  </div>
</div>
<a href="/wiki/Категория:Животные_по_алфавиту?pagefrom=Бобр" title="Категория:Животные по алфавиту">Следующая страница</a>
"""

HTML_WITHOUT_NEXT = """
<div class="mw-category">
  <div class="mw-category-group">
    <ul>
      <li><a href="/wiki/Волк">Волк</a></li>
      <li><a href="/wiki/Выдра">Выдра</a></li>
    </ul>
  </div>
</div>
"""

@pytest.mark.asyncio
async def test_parse_page_with_next():
    counts, next_url = await parse_page(HTML_WITH_NEXT)

    assert isinstance(counts, defaultdict)
    assert counts["А"] == 2
    assert counts["Б"] == 1
    assert next_url is not None
    assert "pagefrom=Бобр" in next_url

@pytest.mark.asyncio
async def test_parse_page_without_next():
    counts, next_url = await parse_page(HTML_WITHOUT_NEXT)

    assert counts["В"] == 2
    assert next_url is None
if __name__ == "__main__":
    asyncio.run(main())
