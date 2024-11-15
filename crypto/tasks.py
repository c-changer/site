from celery import shared_task
import requests
from decimal import Decimal

from .models import Crypto, Bank

from decimal import Decimal, ROUND_DOWN

from app.settings import CoinMarketCup

@shared_task
def kukoin_price():
    #Crypto
    coinList = Crypto.objects.all()

    usdt = Crypto.objects.get(symbol="USDT")
    
    for coin in coinList:
        crypto_objects = Crypto.objects.filter(symbol=coin, is_available=True)

        if not crypto_objects.exists():
            print(coin)
            continue  # Skip iteration if no matching coin is found

        for obj in crypto_objects:
            kukoin_url = f"https://api.kucoin.com/api/v1/market/stats?symbol={obj.symbol}-USDT"
            response = requests.get(kukoin_url)

            data = response.json()
            data = data.get('data')
            price = data.get('last', '0')
            print(price)
            if price != None:
                obj.price = Decimal(price) * usdt.price
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
                
    #Fiat
    fiatList = Bank.objects.all()
    for fiat in fiatList:
        obj = Bank.objects.filter(symbol=fiat, is_available=True).first()

        if not obj:
            print(fiat)
            continue 
        
        kukoin_url = f"https://api.kucoin.com/api/v1/prices?base={obj}&&currencies=USDT"
        response = requests.get(kukoin_url)

        if response.status_code == 200:
            data = response.json()
            data = data.get('data')

            if data is not None:
                price = data.get('USDT', '0')
                print(price)

                obj.price = price
                obj.save()
            else:
                print("No data in response")
        else:
            print(f"Error: {response.status_code}")

    
    

