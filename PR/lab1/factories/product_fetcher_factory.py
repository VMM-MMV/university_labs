import fetchers.steam_fetcher as steam_fetcher

def get_fetcher(fetch_type):
    match fetch_type:
        case "steam":
            return steam_fetcher
        case _:
            raise ValueError(f"Unknown fetcher type: {fetch_type}")