from scraper import Mangakakalot
import pprint
import time
import json
import requests
from pathlib import Path

ROOT_PATH = Path("manga_store")
CONTENTS_PATH = ROOT_PATH / "contents"

CONTENTS_PATH.mkdir(parents=True, exist_ok=True)

manga_source = Mangakakalot()
res = manga_source.latest_manga()

for manga in res["results"]:
    manga_id = manga.get("mangaID")
    if manga_id is None:
        continue

    manga_path = CONTENTS_PATH / manga_id
    manga_path.mkdir(exist_ok=True)

    info = manga_source.manga_info(manga_id=manga_id)
    with open(manga_path / "info.json", "w", encoding="utf-8") as f:
        json.dump(info["results"], f, indent=2, ensure_ascii=False)
