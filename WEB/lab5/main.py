import socket
import traceback
import ssl

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

def send_request(protocol, host, path, headers=None, method='GET'):
    def build_request(method, host, path, headers=None):
        if not headers:
            headers = {}
        
        if 'Host' not in headers:
            headers['Host'] = host
        if 'Connection' not in headers:
            headers['Connection'] = 'close'
        
        request = f"{method} {path} HTTP/1.1\r\n"
        for key, value in headers.items():
            request += f"{key}: {value}\r\n"
        request += "\r\n"
        
        return request.encode('utf-8')
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s.settimeout(10)
    
    port = 443 if protocol == 'https' else 80
    
    try:
        s.connect((host, port))

        if protocol == 'https':
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=host)

        request = build_request(method, host, path, headers)
        
        s.sendall(request)
        
        chunks = []
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
        
        s.close()
        
        response = b''.join(chunks).decode('utf-8', errors='replace')
        
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return None
    


if __name__ == "__main__":
    url = "https://else.fcim.utm.md/login/"
    protocol, host, path = parse_url(url)
    response = send_request(protocol, host, path)
    print(response)