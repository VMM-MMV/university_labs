from managers.product_manager import fetch_products, process_products
from util.file_system import write_json

products = list(fetch_products('https://store.steampowered.com/explore/new/'))
processed_data = process_products(products, min_price=100, max_price=500)
write_json(processed_data, "resources/data.json")

print(processed_data)