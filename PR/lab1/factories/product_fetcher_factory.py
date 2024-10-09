import managers.steam_manager as steam_manager

def get_fetcher(fetch_type):
    match fetch_type:
        case "steam":
            return steam_manager
        case _:
            raise ValueError(f"Unknown fetcher type: {fetch_type}")