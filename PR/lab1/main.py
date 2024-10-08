from bs4 import BeautifulSoup
from http_sender import get_html_content
from exchange_manager import get_exchange_rate
import time

def get_reviews(link):
    try:
        game_page_html = get_html_content(link)
        soup = BeautifulSoup(game_page_html, 'html.parser')
        reviews = soup.find("span", class_="game_review_summary").text

        # if a review has a int, it does not have enough votes to be reviewed
        review_has_int = any(char.isdigit() for char in reviews)
        if review_has_int: return "Not Enough"
        return reviews
    except:
        return None

def get_processed_price(full_price):
    if "free" in full_price.lower(): return 0

    full_price = float(full_price.split("$")[1])
    exchange_rate = get_exchange_rate("usd")
    return round(full_price * exchange_rate, 3)

url = 'https://store.steampowered.com/explore/new/'

html_content = get_html_content(url)
soup = BeautifulSoup(html_content, 'html.parser')

games = soup.find_all('a', class_='tab_item')

for game in games:
    full_price = game.find('div', class_="discount_final_price").text
    price = get_processed_price(full_price)

    name = game.find('div', class_="tab_item_name").text.strip()
    link = game.get('href').strip()
    
    reviews = get_reviews(link)
    print(name, price, reviews, link)
    time.sleep(0.5)