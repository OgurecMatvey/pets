import cloudscraper
import time
import json

def search_wb(product_name, min_price=None, max_price=None):
    scraper = cloudscraper.create_scraper()
    geo_url = "https://www.wildberries.ru/geo/get-form"
    geo_response = scraper.get(geo_url)
    if geo_response.status_code == 200:
        try:
            geo_data = geo_response.json()
            dest = geo_data.get('dest', '-1257786')
        except:
            dest = '-1257786'
    else:
        dest = '-1257786'
    search_url = "https://search.wb.ru/exactmatch/ru/common/v4/search"
    products = []
    page = 1
    total_products = 0

    while True:
        params = {
            'appType': '1',
            'curr': 'rub',
            'dest': dest,
            'query': product_name,
            'resultset': 'catalog',
            'sort': 'priceup',
            'spp': '0',
            'suppressSpellcheck': 'false',
            'priceU': f"{int(min_price * 100) if min_price is not None else ''};{int(max_price * 100) if max_price is not None else ''}",
            'page': str(page),
            'locale': 'ru',
            'lang': 'ru'
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Origin': 'https://www.wildberries.ru',
            'Referer': 'https://www.wildberries.ru/catalog/0/search.aspx'
        }
        response = scraper.get(search_url, params=params, headers=headers)
        if response.status_code != 200:
            break
        try:
            data = response.json()
            if 'data' not in data or 'products' not in data['data'] or not data['data']['products']:
                break
            for item in data['data']['products']:
                name = item.get('name', 'Нет названия')
                price = item.get('salePriceU', 0) / 100
                print(f"Название: {name}")
                print(f"Цена: {price:,.2f} ₽")
                print("-" * 50)
                products.append({
                    'name': name,
                    'price': f"{price:,.2f} ₽"
                })
                total_products += 1
                if total_products >= 100:
                    return products
            page += 1
            time.sleep(0.5)
        except json.JSONDecodeError:
            break
    return products



product_name = str(input("Введите название товара: "))
min_price = float(input("Введите минимальную цену (Enter для пропуска): ") or 0)
max_price = float(input("Введите максимальную цену (Enter для пропуска): ") or 0)
min_price = min_price if min_price > 0 else None
max_price = max_price if max_price > 0 else None

print("Wildberries:")
products = search_wb(product_name, min_price, max_price)

