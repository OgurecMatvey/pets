import requests
import json
from urllib.parse import quote
def search_ozon(product_name, min_price=None, max_price=None):
    search_url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2"
    url_params = f"/search/?text={quote(product_name)}"
    if min_price is not None or max_price is not None:
        url_params += f"&price={min_price or ''}-{max_price or ''}"

    params = {
        "url": url_params
    }

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Origin': 'https://www.ozon.ru',
        'Referer': f'https://www.ozon.ru/search/?text={quote(product_name)}'
    }
    try:
        response = requests.get(search_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            products = []
            widgets = data.get("widgetStates", {})

            for widget_name, widget_value in widgets.items():
                if "searchResultsV2" in widget_name:
                    search_results = json.loads(widget_value)
                    items = search_results.get("items", [])
                    for item in items[:5]:
                        product_info = item.get("cellTrackingInfo", {}).get("product", {})
                        name = product_info.get("title", "Нет названия")
                        price = float(product_info.get("finalPrice", 0))
                        print(f"Название: {name}")
                        print(f"Цена: {price:,.2f} ₽")
                        print("-" * 50)
                        products.append({
                            'name': name,
                            'price': f"{price:,.2f} ₽"
                        })
                    break
            return products
        else:
            print(f"Не удалось получить данные с Ozon. Код ответа: {response.status_code}")
            return []
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return []

product_name = str(input("Введите название товара: "))
min_price = float(input("Введите минимальную цену (Enter для пропуска): ") or 0)
max_price = float(input("Введите максимальную цену (Enter для пропуска): ") or 0)
min_price = min_price if min_price > 0 else None
max_price = max_price if max_price > 0 else None
print("Ozon:")
products = search_ozon(product_name, min_price, max_price)



