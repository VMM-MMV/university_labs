from util.file_system import write_json
from managers.product_manager import process_products
from managers.steam_manager import fetch_products

products = fetch_products()
processed_data = process_products(products, min_price=100, max_price=500)
write_json(processed_data, "resources/data.json")

print(processed_data)