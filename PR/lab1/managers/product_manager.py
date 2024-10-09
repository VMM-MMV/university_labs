from functools import reduce
from datetime import datetime, timezone
from managers.exchange_manager import get_exchange_rate
from managers.currency_manager import get_amount_and_code
from managers.steam_manager import fetch_products

def process_products(products, min_price, max_price):
    def process_price(products):
        full_price = products["price"]

        if "free" in full_price.lower():
            products["price"] = 0
            return products

        amount, currency_code = get_amount_and_code(full_price)
        products["price"] = round(amount * get_exchange_rate(currency_code), 2)
        return products

    def filter_by_price_range(product, min_price, max_price):
        return min_price <= product['price'] <= max_price

    def sum_prices(acc, product):
        return acc + product['price']
    
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
    products = fetch_products()
    processed_data = process_products(products, min_price=100, max_price=500)
    print(processed_data)