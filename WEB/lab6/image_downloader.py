import requests

def download_image(img_link, img_path):
    headers = {
        "accept": "image/webp,image/apng,*/*;q=0.8",
        "referer": "https://www.mangakakalot.gg/"
    }

    response = requests.get(img_link, headers=headers)

    if response.status_code == 200:
        with open(img_path, "wb") as f:
            f.write(response.content)
    elif response.status_code == 304:
        print("Image not modified (HTTP 304), using cached version.")
    else:
        print(f"Failed to download image, status code: {response.status_code}")

if __name__ == "__main__":
    url = "https://img-r1.2xstorage.com/thumb/nerd-project.webp"
    download_image(url, "res.png")
