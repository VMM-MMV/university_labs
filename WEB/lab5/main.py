from http_client import HTTPClient

if __name__ == "__main__":
    client = HTTPClient(use_cache=True)
    url = "https://fcim.utm.md/procesul-de-studii/orar/"
    response = client.request(url)