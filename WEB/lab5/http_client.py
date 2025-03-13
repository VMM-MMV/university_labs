import socket
import ssl
import re
import json
from bs4 import BeautifulSoup
import traceback

class HTTPClient:
    def __init__(self):
        pass
    
    def parse_url(self, url):
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
    
    def build_request(self, method, host, path, headers=None):
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
    
    def is_redirect(self, response):
        status_line = response.split('\n')[0]
        status_match = re.search(r'HTTP/\d\.\d (\d+)', status_line)
        if status_match:
            status_code = int(status_match.group(1))
            return 300 <= status_code < 400
        return False
    
    def get_redirect_location(self, response):
        location_match = re.search(r'Location: (.*?)[\r\n]', response)
        if location_match:
            return location_match.group(1).strip()
        return None
    
    def send_request(self, protocol, host, path, headers=None, method='GET', timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.settimeout(timeout)
        
        port = 443 if protocol == 'https' else 80
        
        try:
            s.connect((host, port))
    
            if protocol == 'https':
                context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=host)
    
            request = self.build_request(method, host, path, headers)
            
            s.sendall(request)
            
            chunks = []
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
            
            s.close()
            
            response = b''.join(chunks).decode('utf-8', errors='replace')
    
            if self.is_redirect(response):
                redirect_url = self.get_redirect_location(response)
                if redirect_url:
                    print(f"Redirecting to: {redirect_url}")
                    protocol, host, path = self.parse_url(redirect_url)
                    return self.send_request(protocol, host, path, headers, method)
            
            return response
            
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return None
    
    def extract_body(self, response):
        if '\r\n\r\n' in response:
            headers, body = response.split('\r\n\r\n', 1)
        else:
            headers, body = response.split('\n\n', 1)
        
        content_type = "text/html"
        content_type_match = re.search(r'Content-Type: (.*?)[\r\n]', headers, re.IGNORECASE)
        if content_type_match:
            content_type = content_type_match.group(1).strip()
        
        if 'application/json' in content_type:
            try:
                parsed = json.loads(body)
                return json.dumps(parsed, indent=2)
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                traceback.print_exc()
                return body
        elif 'text/html' in content_type:
            try:
                soup = BeautifulSoup(body, 'html.parser')
                return " ".join(soup.get_text().split())
            except Exception as e:
                print(f"Error parsing HTML: {e}")
                traceback.print_exc()
                return body
        else:
            return body
    
    def request(self, url, method="GET", headers=None):
        protocol, host, path = self.parse_url(url)
        response = self.send_request(protocol, host, path, headers=headers, method=method)
        
        if not response:
            return "Failed to get response"
        
        return self.extract_body(response)
