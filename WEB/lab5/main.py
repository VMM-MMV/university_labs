from http_client import HTTPClient
import argparse
import json

if __name__ == "__main__":
    query = "python programming"
    client = HTTPClient()
    parser = argparse.ArgumentParser(description="Client command-line interface.")
    
    parser.add_argument("input", help="The input value")
    parser.add_argument("-u", action="store_true", help="Send request to client")
    parser.add_argument("--j", action="store_true", help="Response in JSON format")
    parser.add_argument("--h", action="store_true", help="Response in HTML format")
    parser.add_argument("-s", action="store_true", help="Perform search or open buffer site")
    
    args = parser.parse_args()
    
    if args.u:
        if args.j:
            res = client.request(args.input, headers={"Accept": "application/json"})
            print(json.dumps(res, indent=2))
        else:
            res = client.request(args.input, headers={"Accept": "text/html"})
            print(res)
    elif args.s:
        if args.input.isdigit():
            client.open_buffer_site(int(args.input))
        else:
            client.pretty_search(args.input)
    else:
        parser.print_help()