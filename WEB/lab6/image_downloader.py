import requests

def download_image(img_link, img_path):
    headers = {
        "accept": "image/webp,image/apng,*/*;q=0.8",
        "referer": "https://www.mangakakalot.gg/"
    }

    try:
        response = requests.get(img_link, headers=headers, timeout=2)

        if response.status_code == 200:
            with open(img_path, "wb") as f:
                f.write(response.content)
            return True
        elif response.status_code == 304:
            print("Image not modified (HTTP 304), using cached version.")
        else:
            print(f"Failed to download image, status code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("Request timed out after 2 seconds.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return False

if __name__ == "__main__":
    url = "https://imgs-2.2xstorage.com/a-high-school-boy-reincarnates-as-the-villainous-daughter-in-an-otome-game/3/29.webp"
    download_image(url, "res.png")
