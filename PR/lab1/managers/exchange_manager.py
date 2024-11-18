from bs4 import BeautifulSoup
from util.http_sender import get_html_content
from util.file_system import write_json, read_json
from util.time_calc import get_formated_time, is_older_than_x_hours

def get_exchange_rate(currency_code):
    def get_new_exchange_rate(currency_code):
        html_content = get_html_content("https://www.curs.md/en/curs_valutar/oficial")
        soup = BeautifulSoup(html_content, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows:
            # Find the currency code in the row
            currency = row.find('span', class_=f"moneda {currency_code.lower()}")
            if currency:
                # Get the rate, which is in the third 'td' element
                rate = row.find_all('td')[2].text
                return float(rate)
        
        return None
    
    currency_code = currency_code.lower()

    exchange_records = 'resources/exchange_rates.json'
    json_data = read_json(exchange_records)

    # Update if date is older than 24 hours or currency does not exist in json
    if is_older_than_x_hours(json_data.get("date"), 24) or json_data.get(currency_code) == None:
        json_data["date"] = get_formated_time()
        json_data[currency_code] = get_new_exchange_rate(currency_code)
        write_json(json_data, exchange_records)
    
    return json_data[currency_code]

if __name__ == "__main__":
    a = get_exchange_rate("EUR")
    print(a)