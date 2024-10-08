from bs4 import BeautifulSoup
from http_sender import get_html_content
from exchange_manager import get_exchange_rate
from datetime import datetime, timezone
from functools import reduce

def fetch_products(url):
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    games = soup.find_all('a', class_='tab_item')

    for game in games:
        price = game.find('div', class_="discount_final_price").text
        name = game.find('div', class_="tab_item_name").text.strip()
        link = game.get('href').strip()
        reviews = get_reviews(link)
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

def process_price(full_price):
    if "free" in full_price.lower():
        return 0

    full_price = float(full_price.split("$")[1])
    exchange_rate = get_exchange_rate("usd")
    return round(full_price * exchange_rate, 2)

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
    result = {
        "filtered_products": filtered_products,
        "total_price": round(total_price, 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    return result

if __name__ == "__main__":
    products = list(fetch_products('https://store.steampowered.com/explore/new/'))
    processed_data = process_products(products, min_price=10, max_price=50)
    print(processed_data)