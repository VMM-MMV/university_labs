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

main_json = []
for manga in res["results"]:
    manga_id = manga.get("mangaID")
    if manga_id is None: continue

    current_manga = {
        "title" : manga.get("title"),
        "latestChapter" : manga.get("latestChapter"),
        "views" : manga.get("view"),
        "description" : manga.get("description")
    }

    manga_path = CONTENTS_PATH / manga_id
    manga_path.mkdir(exist_ok=True)

    info = manga_source.manga_info(manga_id=manga_id)
    info_path = manga_path / "info.json"
    with open(info_path, "w", encoding="utf-8") as f:
        json.dump(info["results"], f, indent=2, ensure_ascii=False)


    img_path = manga_path / "img.webp"
    current_manga["img_path"] = str(img_path)

    download_image(img_link=manga["img"], img_path=img_path)

    
    chapter = info["results"]["chapters"][0]
    chapter_info = manga_source.fetch_chapter(chapter.get("chapterID"))
    chapter_path = manga_path / chapter.get("chapterName")
    chapter_path.mkdir(exist_ok=True)

    current_manga["latestChapter"] = str(chapter_path)

    print("Processing chapter", chapter)

    for i, img_link in enumerate(chapter_info["results"]["primary_imgs"]):
        img_path = chapter_path / f"{i}.webp"
        downloaded_succesfuly = download_image(img_link=img_link, img_path=img_path)
        if not downloaded_succesfuly:
            img_link = chapter_info["results"]["secondary_imgs"][i]
            download_image(img_link=img_link, img_path=img_path)

    main_json.append(current_manga)

with open(ROOT_PATH / "store.json", "w", encoding="utf-8") as f:
    json.dump(main_json, f, indent=2, ensure_ascii=False)