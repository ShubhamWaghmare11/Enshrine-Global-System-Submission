import requests
from google.adk.tools import ToolContext
from google.adk.agents import Agent

def get_crypto_market_data(coin_id: str, tool_context: ToolContext, vs_currency: str = "usd", days: int=1) -> dict:
    """Fetches cryptocurrency market data from CoinGecko for provided Coin id. and provided currency type and past n days data"""
    try:
        
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}")
        response.raise_for_status()
        data = response.json()
        latest_price = data["prices"][-1][1]  # Latest price

        latest_change = (data["market_caps"][-1][1] / data["market_caps"][0][1]) - 1  # 24h change
        crypto_data = {
            "status": "success",
            "coin_id": coin_id,
            "date": "current",
            "price_usd": latest_price,
            "market_change_24h": f"{latest_change * 100}%"  # As percentage
        }

        tool_context.state['crypto_data'] = crypto_data

        return crypto_data
    
    except Exception as e:
        return {"status": "error", "error_message": str(e)}



coingecko_agent = Agent(
    name="coingecko_agent",
    model="gemini-2.0-flash",
    description="An agent that retrieves cryptocurrency market data such as price and market cap change using CoinGecko. It does NOT provide crypto news or general information.",
    instruction="""
    You are the Crypto Price Agent. Your only task is to fetch market data (price, 24h market cap change) for a specified cryptocurrency using CoinGecko's market_chart API endpoint. Do NOT handle any queries related to crypto news, regulations, or trends.

    Store the data in ToolContext under the key 'crypto_data' with the following structure:
    {
        'status': 'success',
        'coin_id': <coin_id>,
        'date': <requested date or 'current'>,
        'price_usd': <latest price>,
        'market_change_24h': <percentage change in market cap over the time period>
    }
    """,
    tools=[get_crypto_market_data]
)