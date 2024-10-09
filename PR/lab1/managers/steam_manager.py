from bs4 import BeautifulSoup
from util.http_sender import get_html_content

def fetch_products(url='https://store.steampowered.com/explore/new/'):
    return yield_products(url)

def yield_products(url='https://store.steampowered.com/explore/new/'):
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    games = soup.find_all('a', class_='tab_item')

    for game in games:
        try:
            price = game.find('div', class_="discount_final_price").text
            name = str(game.find('div', class_="tab_item_name").text.strip())
            link = str(game.get('href').strip())
            reviews = get_reviews(link)
            print(price, name, link, reviews)
            
            yield {"name": name, "price": price, "reviews": reviews, "link": link}
        except:
            pass

def get_reviews(link):
    try:
        game_page_html = get_html_content(link)
        soup = BeautifulSoup(game_page_html, 'html.parser')
        reviews = soup.find("span", class_="game_review_summary").text

        review_has_int = any(char.isdigit() for char in reviews)
        if review_has_int:
            return "Not Enough"
        return reviews
    except:
        return None