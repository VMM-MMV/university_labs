import requests
import concurrent.futures

# Define the URL of the endpoint
url = 'http://localhost:8080/content'

# Define the payloads for each request
payloads = [
    {"content": "Sample content 10", "type": "WRITE"},
    {"content": "hello", "type": "READ"},
    {"content": "Sample content 8", "type": "WRITE"}
]

# Function to send a POST request
def send_request(payload):
    try:
        response = requests.post(url, json=payload)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

# Execute 3 requests concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    # Map the function with the payloads
    futures = [executor.submit(send_request, payload) for payload in payloads]

    # Print results as they complete
    for future in concurrent.futures.as_completed(futures):
        status_code, response_text = future.result()
        print(f"Status Code: {status_code}, Response: {response_text}")
