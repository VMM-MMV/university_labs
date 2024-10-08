from bs4 import BeautifulSoup
from http_sender import get_html_content
import time

url = 'https://store.steampowered.com/explore/new/'

html_content = get_html_content(url)
soup = BeautifulSoup(html_content, 'html.parser')

games = soup.find_all('a', class_='tab_item')

for game in games:
    price = game.find('div', class_="discount_final_price").text
    name = game.find('div', class_="tab_item_name").text
    link = game['href']
    try:
        game_page_html = get_html_content(link)
        soup = BeautifulSoup(game_page_html, 'html.parser')
        reviews = soup.find("span", class_="game_review_summary").text
        if any(char.isdigit() for char in reviews):
            reviews = "Not Enough"
    except:
        reviews = None
    print(reviews)
    # time.sleep(1)
    # break