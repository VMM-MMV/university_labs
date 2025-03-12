def parse_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        
    protocol = 'https' if 'https://' in url else 'http'
    url = url.replace('http://', '').replace('https://', '')
    
    if '/' in url:
        host, path = url.split('/', 1)
        path = '/' + path
    else:
        host = url
        path = '/'
        
    return protocol, host, path

if __name__ == "__main__":
    url = "https://else.fcim.utm.md/login/"
    purl = parse_url(url)
    print(purl)