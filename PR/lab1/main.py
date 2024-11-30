from util.file_system import write_json
from managers.product_manager import process_products
from factories.product_fetcher_factory import get_fetcher
from rabbit_uploader import publish_message
from ftp_uploader import upload_json
import random

fetcher = get_fetcher("steam")
products = fetcher.fetch_products(max_items=5)
publish_message(str(list(products)))
processed_data = process_products(products, min_price=100, max_price=500)
upload_json(processed_data, "file_" + str(random.randint(1, 10000)) + ".txt")
write_json(processed_data, "resources/data.json")

print(processed_data)
