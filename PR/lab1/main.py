from product_manager import fetch_products, process_products

products = list(fetch_products('https://store.steampowered.com/explore/new/'))
processed_data = process_products(products, min_price=10, max_price=50)
print(processed_data)