from http_sender import get_html_content
from bs4 import BeautifulSoup

html_content = get_html_content("https://www.cursbnm.md/curs-dolar")

soup = BeautifulSoup(html_content, 'html.parser')

exchange_rate_element = float(soup.find('strong').text.split("=")[1].strip().split(" ")[0].replace(",","."))

print(exchange_rate_element)