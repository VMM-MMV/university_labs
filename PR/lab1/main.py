from util.file_system import write_json
from managers.product_manager import process_products
from factories.product_fetcher_factory import get_fetcher

fetcher = get_fetcher("steam")
products = fetcher.fetch_products()
processed_data = process_products(products, min_price=100, max_price=500)
write_json(processed_data, "resources/data.json")

print(processed_data)