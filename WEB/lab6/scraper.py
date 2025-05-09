import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class Mangakakalot:
    def __init__(self):
        self.url = "https://www.mangakakalot.gg"

    def latest_manga(self, page=1):
        response = requests.get(f"{self.url}/manga-list/latest-manga?page={page}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for item in soup.select('.truyen-list .list-truyen-item-wrap'):
                manga_id = item.select_one('a')['href'].replace('/manga/', '').replace(self.url, "")
                img = f"{item.select_one('a img')['data-src']}"
                title = item.select_one('a')['title']
                latest_chapter_tag = item.select('a')[2] if len(item.select('a')) > 2 else None
                latest_chapter = latest_chapter_tag['title'] if latest_chapter_tag and 'title' in latest_chapter_tag.attrs else "N/A"
                chapter_id = latest_chapter_tag['href'].replace('/chapter/', '') if latest_chapter_tag and 'href' in latest_chapter_tag.attrs else "N/A"
                view = item.select_one('.aye_icon').get_text(strip=True)
                description = description_tag.get_text(strip=True) if (description_tag := item.select_one('p')) else "N/A"
                results.append({
                    'mangaID': manga_id,
                    'img': img,
                    'title': title,
                    'latestChapter': latest_chapter,
                    'chapterID': chapter_id,
                    'view': view,
                    'description': description
                })

            current_page = soup.select_one('.panel_page_number .group_page .page_select').get_text(strip=True)
            total_page_href = soup.select_one('.panel_page_number .group_page .page_last:last-of-type')['href']
            parsed_url = urlparse(total_page_href)
            page_number = parse_qs(parsed_url.query).get('page', [''])[0]
            results.append({'page': current_page, 'totalPage': page_number})
            return {'results': results}
        raise Exception(f"{response.status_code}")

    def search(self, query, page=1):
        if not query:
            raise Exception("Missing query!")
        page = max(int(page), 1)
        response = requests.get(f"{self.url}/search/story/{query}?page={page}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            manga_list = []
            for item in soup.select('.daily-update .panel_story_list .story_item'):
                full_url = item.select_one('a')['href']
                manga_id = full_url.split('/manga/')[1]
                thumbnail = item.select_one('a img')['src']
                title = item.select_one('.story_name a').get_text(strip=True)
                author = item.select_one('.story_item_right span:-soup-contains("Author")').get_text(strip=True).replace('Author(s) : ', '')
                update = item.select_one('.story_item_right span:-soup-contains("Updated")').get_text(strip=True).replace('Updated : ', '')
                view = item.select_one('.story_item_right span:-soup-contains("View")').get_text(strip=True).replace('View : ', '')
                manga_info = {
                    'id': manga_id,
                    'img': thumbnail,
                    'title': title,
                    'author': author,
                    'update': update,
                    'view': view
                }
                manga_list.append(manga_info)
            current_page = soup.select_one('.panel_page_number .group_page .page_select').get_text(strip=True)
            total_page_href = soup.select_one('.panel_page_number .group_page .page_last:last-of-type')['href']
            parsed_url = urlparse(total_page_href)
            page_number = parse_qs(parsed_url.query).get('page', [''])[0]
            return {
                'results': manga_list,
                'pages': [{'page': current_page, 'totalPage': page_number, 'searchKey': query}]
            }
        raise Exception(f"{response.status_code}")

    def manga_info(self, manga_id):
        if not manga_id:
            raise Exception("Missing id!")
        response = requests.get(f"{self.url}/manga/{manga_id}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            thumbnail = soup.select_one('.manga-info-top .manga-info-pic img')['src']
            title = soup.select_one('.manga-info-top .manga-info-text li:nth-of-type(1) h1').get_text(strip=True)
            authors = [a.get_text(strip=True) for a in soup.select('.manga-info-top .manga-info-text li:-soup-contains("Author(s)") a')]
            status = soup.select_one('.manga-info-top .manga-info-text li:nth-of-type(2)').get_text(strip=True).replace('Status : ', '')
            last_update = soup.select_one('.manga-info-top .manga-info-text li:nth-of-type(3)').get_text(strip=True).replace('Last updated : ', '')
            view = soup.select_one('.manga-info-top .manga-info-text li:nth-of-type(5)').get_text(strip=True).replace('View : ', '')
            genres = [a.get_text(strip=True) for a in soup.select('.manga-info-top .manga-info-text li:-soup-contains("Genres") a')]

            # Parse rating
            rating = {'score': 0, 'outOf': 5, 'votes': 0}
            json_ld_tag = soup.find('script', type='application/ld+json')
            if json_ld_tag:
                try:
                    import json
                    rating_data = json.loads(json_ld_tag.string)
                    rating = {
                        'score': float(rating_data.get('ratingValue', 0)),
                        'outOf': 5,
                        'votes': int(rating_data.get('ratingCount', 0))
                    }
                except Exception:
                    pass

            summary = soup.select_one('#contentBox').get_text(strip=True)
            chapters = []
            for row in soup.select('.chapter .manga-info-chapter .chapter-list .row'):
                chapter_name = row.select_one('a').get_text(strip=True)
                chapter_id_url = row.select_one('a')['href']
                chapter_id = chapter_id_url.split('/manga/')[1]
                views = row.select_one('span:nth-of-type(2)').get_text(strip=True)
                time_uploaded = row.select_one('span:nth-of-type(3)').get_text(strip=True)
                chapters.append({
                    'chapterName': chapter_name,
                    'chapterID': chapter_id,
                    'views': views,
                    'timeUploaded': time_uploaded
                })

            return {
                'results': {
                    'img': thumbnail,
                    'title': title,
                    'authors': authors,
                    'status': status,
                    'lastUpdate': last_update,
                    'view': view,
                    'genres': genres,
                    'rating': rating,
                    'summary': summary,
                    'chapters': chapters
                }
            }
        raise Exception(f"{response.status_code}")

if __name__ == "__main__":
    mangakakalot = Mangakakalot()
    res = mangakakalot.latest_manga()
    print(res)