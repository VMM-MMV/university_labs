import socket 
import ssl 
import json  
import re 
import bs4
def remove_8_char_sequences(text): 
    # Regular expression to match any sequence of exactly 8 hexadecimal digits 
    return re.sub(r'\b[0-9a-fA-F]{8}\b', '', text) 
 
def send_https_request(host, port=443, path='/'): 
    try: 
        # 1. Create a TCP socket 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
 
        # 2. Wrap the socket in an SSL context for HTTPS 
        context = ssl.create_default_context() 
        secure_sock = context.wrap_socket(sock, server_hostname=host) 
 
        # 3. Connect to the host and port 
        secure_sock.connect((host, port)) 
        print(path) 
 
        # 4. Prepare the HTTPS request string with the path 
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: PythonSocket\r\nConnection: close\r\n\r\n" 
 
        # 5. Send the HTTPS request through the secure socket 
        secure_sock.sendall(request.encode()) 
 
        # 6. Receive the response 
        response = b"" 
        while True: 
            chunk = secure_sock.recv(24000) 
            if not chunk: 
                break 
            response += chunk 
 
        # Close the secure socket connection 
        secure_sock.close() 
 
        # 7. Decode the response and separate headers from the  
        # response = response.decode('utf-8') 
        # response = remove_8_char_sequences(response) 
        response = str(response)
        print(response)
        headers, body = response.split('\r\n\r\n', 1) 
 
        # Output the HTTP body (you can process it further) 
        print(body) 
        return json.loads(body)["results_html"] 
 
    except socket.error as e: 
        print(f"Socket error: {e}") 
    except ssl.SSLError as ssl_err: 
        print(f"SSL error: {ssl_err}") 
 
if __name__ == "__main__":
    host = "carturesti.ro" 
    port = 443 
    html = send_https_request(host, port, "/raft/carte-109")
    print(html)
    # for i in range(10): 
    #     path = f"/market/search/render/?query=&start={i}&count={i*10+1}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=570" 
    #     response=send_https_request(host, port, path) 
        # print(response