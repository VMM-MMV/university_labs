from scraper import Mangakakalot
import pprint
import time
import json
import requests
from pathlib import Path
from image_downloader import download_image

ROOT_PATH = Path("manga_store")
CONTENTS_PATH = ROOT_PATH / "contents"

CONTENTS_PATH.mkdir(parents=True, exist_ok=True)

manga_source = Mangakakalot()
res = manga_source.latest_manga()

for manga in res["results"]:
    manga_id = manga.get("mangaID")
    if manga_id is None: continue

    manga_path = CONTENTS_PATH / manga_id
    manga_path.mkdir(exist_ok=True)

    # info = manga_source.manga_info(manga_id=manga_id)
    # info_path = manga_path / "info.json"
    # with open(info_path, "w", encoding="utf-8") as f:
    #     json.dump(info["results"], f, indent=2, ensure_ascii=False)

    img_path = manga_path / "img.webp"
    print(manga["img"])
    download_image(img_link=manga["img"], img_path=img_path)
    
