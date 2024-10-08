hostname = 'https://store.steampowered.com/'
port = 443 if hostname.find("https") != -1 else 80
host_start = hostname.find("//") + len("//")
path_start = hostname.find("/", host_start)
host = hostname[host_start:path_start]
path = hostname[path_start:]
print(host, path, port)