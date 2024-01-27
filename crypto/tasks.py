from celery import shared_task
import requests
from decimal import Decimal

from .models import Crypto

from decimal import Decimal, ROUND_DOWN

@shared_task
def binance_price():
    coinList = Crypto.objects.all()


    for coin in coinList:
        try:
            obj = Crypto.objects.get(symbol=coin)
        except Crypto.DoesNotExist:
            print(coin)
            continue  # Пропустить итерацию, если монета не найдена

        binance_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={obj.symbol}USDT"
        response = requests.get(binance_url)
        if response.status_code == 200:
            data = response.json()  # Parse JSON response
            price = data.get('lastPrice', '0')  # Get the 'price' field from the JSON data
            price = Decimal(price)
            obj.price = price        
        else:
            url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
            params = {
                'start': '1',      # Start index of the cryptocurrency data
                'limit': '1000',    # Number of cryptocurrencies to retrieve
                'convert': 'USD'   # Currency to convert the prices to
            }
            headers = {
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': CoinMarketCup
            }
            response = requests.get(url, params=params, headers=headers)

            data = response.json()
            
            if 'data' in data:
                for cryptocurrency in data['data']:
                    symbol = cryptocurrency['symbol']
                    if symbol in coinList:  # Filter specific cryptocurrencies
                        obj.price = cryptocurrency['quote']['USD']['price']
        try:
            obj.save()
        except Exception as e:
            # Handle any additional errors when saving the object
            print(f"Error saving object: {e}")