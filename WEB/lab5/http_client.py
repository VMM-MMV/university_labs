import socket
import ssl
import re
import json
from bs4 import BeautifulSoup
from cache import HttpCache
import traceback
import json
import urllib.parse
import webbrowser
from search_buffer import SearchBuffer
import argparse

class HTTPClient:
    def __init__(self, use_cache=True, cache_dir='.cache'):
        self.use_cache = use_cache
        self.cache = HttpCache(cache_dir) if use_cache else None
        self.search_buffer = SearchBuffer()
    
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

        body = re.sub(r'(?:\r\n|\n|\r)?[0-9a-fA-F]+(?:\r\n|\n|\r)', '', body)
        body = re.sub(r'(?:\r\n|\n|\r)?0(?:\r\n|\n|\r)+$', '', body)

        if 'application/json' in content_type:
            try:
                return json.loads(body)
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

        if self.use_cache and method == 'GET':
            cached_response = self.cache.get_cached_response(host, path, headers)
            if cached_response:
                print(f"Using cached response for {host}{path}")
                return cached_response
            
        response = self.send_request(protocol, host, path, headers=headers, method=method)

        if not response:
            return "Failed to get response"
        
        response_body = self.extract_body(response)

        if self.use_cache and method == 'GET':
            self.cache.cache_response(host, path, headers, str(response_body))
        
        return response_body
    
    def search(self, query, num_results=10):
        encoded_query = urllib.parse.quote(query)
        
        url = f"api.duckduckgo.com/?q={encoded_query}&format=json&t=python_script"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Accept": "application/json"
        }
        
        response = self.request(url, headers=headers)

        data = json.loads(response)
        
        results = []
        
        if data.get('AbstractText'):
            results.append({
                'title': data.get('Heading', 'Abstract'),
                'url': data.get('AbstractURL', ''),
                'snippet': data.get('AbstractText', '')
            })
        
        for topic in data.get('RelatedTopics', [])[:num_results]:
            if 'Text' in topic and 'FirstURL' in topic:
                results.append({
                    'title': topic.get('Text', '').split(' - ')[0] if ' - ' in topic.get('Text', '') else topic.get('Text', ''),
                    'url': topic.get('FirstURL', ''),
                    'snippet': topic.get('Text', '')
                })
            elif 'Topics' in topic:
                for subtopic in topic.get('Topics', [])[:num_results - len(results)]:
                    if len(results) >= num_results:
                        break
                    results.append({
                        'title': subtopic.get('Text', '').split(' - ')[0] if ' - ' in subtopic.get('Text', '') else subtopic.get('Text', ''),
                        'url': subtopic.get('FirstURL', ''),
                        'snippet': subtopic.get('Text', '')
                    })

        self.search_buffer.update_buffer(results[:num_results])
        return results[:num_results]

    def pretty_search(self, query, num_results=10):
        results = self.search(query, num_results)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   {result['snippet']}")
    
    def open_buffer_site(self, index):
        search_buffer = self.search_buffer.get_buffer()
        if not search_buffer:
            print("No searches have been made")
            return
        url = search_buffer[index]['url']
        webbrowser.open(url)