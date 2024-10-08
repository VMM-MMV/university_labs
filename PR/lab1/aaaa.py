import socket
import ssl
from bs4 import BeautifulSoup

def get_html_content(hostname, path, port):
    try:
        # Create a socket
        context = ssl.create_default_context()
        sock = socket.create_connection((hostname, port))

        # Wrap the socket in SSL
        ssl_sock = context.wrap_socket(sock, server_hostname=hostname)

        # Send an HTTP request
        request = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
        ssl_sock.sendall(request.encode('utf-8'))

        # Receive the response
        response = b""
        while True:
            data = ssl_sock.recv(4096)
            if not data:
                break
            response += data
        
        return response.split(b"\r\n\r\n", 1)[1].decode('utf-8')
    finally:
        ssl_sock.close()


# Host and port
hostname = 'carturesti.ro'
path = "/raft/carte-109"
port = 443

html_content = get_html_content(hostname, path, port)
soup = BeautifulSoup(html_content, 'html.parser')

books = soup.find_all('div', class_='cartu-grid-tile')

print(books)