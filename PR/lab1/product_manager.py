from bs4 import BeautifulSoup
from http_sender import get_html_content
from exchange_manager import get_exchange_rate
from datetime import datetime, timezone
from functools import reduce

currency_dict = {
    '€': 'EUR',  # Euro
    '$': 'USD',  # US Dollar
    '£': 'GBP',  # British Pound Sterling
    '¥': 'JPY',  # Japanese Yen
    '₹': 'INR',  # Indian Rupee
    '₩': 'KRW',  # South Korean Won
    '₽': 'RUB',  # Russian Ruble
    '₺': 'TRY',  # Turkish Lira
    '₪': 'ILS',  # Israeli New Shekel
    '₫': 'VND',  # Vietnamese Dong
    '₦': 'NGN',  # Nigerian Naira
    '₴': 'UAH'  # Ukrainian Hryvnia
}

def get_currency_symbol(price_str):
    """Find the currency symbol in the price string."""
    for symbol in currency_dict.keys():
        if symbol in price_str:
            return symbol
    raise ValueError("Currency symbol not recognized in the price string.")

def fetch_products(url):
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    games = soup.find_all('a', class_='tab_item')

    for game in games:
        price = game.find('div', class_="discount_final_price").text
        name = str(game.find('div', class_="tab_item_name").text.strip())
        link = str(game.get('href').strip())
        reviews = get_reviews(link)
        print(price, name, link, reviews)
        
        yield {"name": name, "price": price, "reviews": reviews, "link": link}

def get_reviews(link):
    try:
        game_page_html = get_html_content(link)
        soup = BeautifulSoup(game_page_html, 'html.parser')
        reviews = soup.find("span", class_="game_review_summary").text

        review_has_int = any(char.isdigit() for char in reviews)
        if review_has_int:
            return "Not Enough"
        return reviews
    except:
        return None

def process_price(products):
    full_price = products["price"]

    if "free" in full_price.lower():
        products["price"] = 0
        return products

    currency_symbol = get_currency_symbol(full_price)
    price_value = float(full_price.replace(currency_symbol,"").replace(",","."))
    
    currency_code = currency_dict[currency_symbol]

    exchange_rate = get_exchange_rate(currency_code)    
    products["price"] = round(price_value * exchange_rate, 2)
    return products

def filter_by_price_range(product, min_price, max_price):
    return min_price <= product['price'] <= max_price

def sum_prices(acc, product):
    return acc + product['price']

def process_products(products, min_price, max_price):
    # Map: Convert prices
    converted_products = list(map(process_price, products))

    # Filter: Products within price range
    filtered_products = list(filter(lambda p: filter_by_price_range(p, min_price, max_price), converted_products))

    # Reduce: Sum up prices of filtered products
    total_price = reduce(sum_prices, filtered_products, 0)

    # Create new data structure
    return {
        "filtered_products": filtered_products,
        "total_price": round(total_price, 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    products = list(fetch_products('https://store.steampowered.com/explore/new/'))
    processed_data = process_products(products, min_price=100, max_price=500)
    print(processed_data)