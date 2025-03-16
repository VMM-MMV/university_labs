import os
import time

class HttpCache:
    def __init__(self, cache_dir='.cache'):
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def get_cache_key(self, host, path, headers):
        return f"{host}_{path.replace('/', '_')}_{hash(str(headers)) if headers else ''}"
    
    def get_cached_response(self, host, path, headers):
        cache_key = self.get_cache_key(host, path, headers)
        cache_file = os.path.join(self.cache_dir, cache_key)
        
        if os.path.exists(cache_file):
            if time.time() - os.path.getmtime(cache_file) < 86400:  # 24 hours
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
        return None
    
    def cache_response(self, host, path, headers, response):
        cache_key = self.get_cache_key(host, path, headers)
        cache_file = os.path.join(self.cache_dir, cache_key)
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(response)