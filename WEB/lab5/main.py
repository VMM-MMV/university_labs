from http_client import HTTPClient
import argparse
import json

if __name__ == "__main__":
    query = "python programming"
    client = HTTPClient()
    parser = argparse.ArgumentParser(description="Client command-line interface.")
    
    parser.add_argument("input", help="The input value")
    parser.add_argument("-u", action="store_true", help="Send request to client")
    parser.add_argument("-s", action="store_true", help="Perform search or open buffer site")
    
    args = parser.parse_args()
    
    if args.u:
        res = client.request(args.input)
        print(res)
    elif args.s:
        if args.input.isdigit():
            client.open_buffer_site(int(args.input))
        else:
            client.pretty_search(args.input)
    else:
        parser.print_help()