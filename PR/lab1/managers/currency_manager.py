currency_dict = {
    '€': 'EUR',  # Euro
    '$': 'USD',  # US Dollar
    '£': 'GBP',  # British Pound Sterling
    '¥': 'JPY',  # Japanese Yen
    '₹': 'INR',  # Indian Rupee
    '₩': 'KRW',  # South Korean Won
    '₽': 'RUB',  # Russian Ruble
    '₺': 'TRY',  # Turkish Lira
    '₪': 'ILS',  # Israeli New Shekel
    '₫': 'VND',  # Vietnamese Dong
    '₦': 'NGN',  # Nigerian Naira
    '₴': 'UAH'   # Ukrainian Hryvnia
}

def get_currency_symbol(price_str):
    """Find the currency symbol in the price string."""
    for symbol in currency_dict.keys():
        if symbol in price_str:
            return symbol
    raise ValueError("Currency symbol not in the currency database.")

def get_amount_and_code(full_price):
    currency_symbol = get_currency_symbol(full_price)
    amount = float(full_price.replace(currency_symbol,"").replace(",","."))
    
    currency_code = currency_dict[currency_symbol]
    return amount, currency_code