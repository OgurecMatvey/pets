import cloudscraper
from bs4 import BeautifulSoup
import json
import os

def load_cookies(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл с cookies не найден: {file_path}")
    
    with open(file_path, 'r') as file:
        cookies = json.load(file)
    return {cookie['name']: cookie['value'] for cookie in cookies}

def search_rutracker(query, cookies_file):
    SEARCH_URL = f"https://rutracker.org/forum/tracker.php?nm={query}"
    scraper = cloudscraper.create_scraper()

    cookies = load_cookies(cookies_file)
    scraper.cookies.update(cookies)

    response = scraper.get(SEARCH_URL)
    if response.status_code != 200:
        print("Ошибка при доступе к поиску.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for row in soup.select('.tLink'):
        title = row.text
        link = f"https://rutracker.org/forum/{row['href']}"
        results.append((title, link))

    if not results:
        print("Ничего не найдено.")
        return

    print("\nНайдено:")
    for idx, (title, link) in enumerate(results[:10], 1):
        print(f"{idx}. {title}\n   {link}")

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    
    query = input("Введите запрос для поиска: ")
    cookies_file = os.path.join(current_dir, "cookies.json")
    search_rutracker(query, cookies_file)
