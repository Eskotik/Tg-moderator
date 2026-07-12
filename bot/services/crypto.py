import json
import logging

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from millify import millify

from bot.config import CMC_API_KEY


def get_coin_price(coin_symbol: str) -> str:
    if not CMC_API_KEY:
        return "CoinMarketCap API key is not configured. Add COINMARKETCAP_KEY to .env"

    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {"symbol": coin_symbol.upper()}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        if data.get("status", {}).get("error_code"):
            error_msg = data["status"].get("error_message", "Unknown API error")
            return f"CoinMarketCap Error: {error_msg}"

        if "data" in data and coin_symbol.upper() in data["data"]:
            coin_data = data["data"][coin_symbol.upper()][0]
            name = coin_data["name"]
            price = coin_data["quote"]["USD"]["price"]
            percent_24h = coin_data["quote"]["USD"]["percent_change_24h"]
            volume_24h = coin_data["quote"]["USD"]["volume_24h"]
            market_cap = coin_data["quote"]["USD"]["market_cap"]
            percent_24h_formatted = (
                f"+{percent_24h:.2f}" if percent_24h > 0 else f"{percent_24h:.2f}"
            )
            market_cap_formatted = millify(market_cap, precision=2)
            volume_24h_formatted = millify(volume_24h, precision=2)
            if price > 1:
                price_formatted = f"{price:.2f}"
            elif price > 0.01 and price < 1:
                price_formatted = f"{price:.5f}"
            else:
                price_formatted = f"{price:.9f}"

            return (
                f"{name} ({coin_symbol.upper()}):"
                f" ${price_formatted}\n"
                f"24h Price Change: {percent_24h_formatted}%\n"
                f"24h Trading Volume: ${volume_24h_formatted}\n"
                f"Market Cap: ${market_cap_formatted}"
            )
        else:
            return f"Could not find information for coin {coin_symbol.upper()}"

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Error retrieving data: {e}"
    except KeyError:
        return f"Error: Unexpected data structure in API response for {coin_symbol.upper()}"
