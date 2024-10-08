from datetime import datetime, timedelta
from http_sender import get_html_content
from bs4 import BeautifulSoup
from file_system import write_json, read_json

def get_new_exchange_rate():
    html_content = get_html_content("https://www.cursbnm.md/curs-dolar")

    soup = BeautifulSoup(html_content, 'html.parser')

    return float(soup.find('strong').text.split("=")[1].strip().split(" ")[0].replace(",","."))

def is_older_than_24_hours(stored_date):
    # Function to check if date is older than 24 hours
    current_time = datetime.now()
    time_difference = current_time - stored_date
    return time_difference > timedelta(hours=24)

def get_exchange_rate(currency_type):
    currency_type = currency_type.lower()

    exchange_records = 'exchange_rates.json'
    json_data = read_json(exchange_records)

    stored_date_str = json_data.get("date")
    stored_date = datetime.strptime(stored_date_str, "%Y-%m-%d %H:%M:%S")

    # Update if date is older than 24 hours
    if is_older_than_24_hours(stored_date):
        json_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_data[currency_type] = get_exchange_rate()
        write_json(exchange_records, json_data)
    
    return json_data[currency_type]