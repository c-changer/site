from celery import shared_task
import requests
from decimal import Decimal

from .models import Crypto

from decimal import Decimal, ROUND_DOWN

from app.settings import CoinMarketCup

@shared_task
def binance_price():
    coinList = Crypto.objects.all()

    usdt = Crypto.objects.get(symbol="USDT")
    
    for coin in coinList:
        crypto_objects = Crypto.objects.filter(symbol=coin, is_available=True)

        if not crypto_objects.exists():
            print(coin)
            continue  # Skip iteration if no matching coin is found

        for obj in crypto_objects:
            binance_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={obj.symbol}USDT"
            response = requests.get(binance_url)

            if response.status_code == 200:
                data = response.json()
                price = data.get('lastPrice', '0')
                price = Decimal(price)
                obj.price = price
                print(obj.price)
            else:
                url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
                params = {
                    'start': '1',
                    'limit': '1000',
                    'convert': 'USD'
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
                        if symbol == coin:
                            obj.price = cryptocurrency['quote']['USD']['price']

            try:
                obj.save()
            except Exception as e:
                # Handle any additional errors when saving the object
                print(f"Error saving object: {e}")
