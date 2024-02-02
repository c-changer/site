from django.db.models.signals import post_migrate
from app.settings import CoinMarketCup
from django.dispatch import receiver
import requests
from .models import Crypto, DepositSettings, Exchange

@receiver(post_migrate)
def create_initial_instance(sender, **kwargs):
    if sender.name == 'crypto':
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
        
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()

            if 'data' in data:
                coinList = ['BTC', 'ETH', 'LTC', 'USDT']

                for cryptocurrency in data['data']:
                    symbol = cryptocurrency['symbol']
                    if symbol in coinList:
                        obj, created = Crypto.objects.get_or_create(symbol=symbol)
                        obj.name = cryptocurrency['name']
                        obj.symbol = symbol
                        obj.price = cryptocurrency['quote']['USD']['price']

                        crypto_name = cryptocurrency['name'].lower().replace(" ", "-")
                        icon_url = f"https://cryptologos.cc/logos/{crypto_name}-{symbol.lower()}-logo.svg"
                        response = requests.head(icon_url)  # Send a HEAD request to check the status code
                        if response.status_code == 404:
                            obj.icon = f"https://s2.coinmarketcap.com/static/img/coins/64x64/{cryptocurrency['id']}.png"
                        else:
                            obj.icon = icon_url

                        if cryptocurrency['name'] == "HarryPotterObamaPacMan8Inu":
                            obj.name = "Ripple"

                        print(obj.name)
                        print(obj.price)
                        obj.save()

                        if obj.name == "Tether USDt":
                            obj.name = "Tether"
                        if obj.symbol == 'XRP':
                            obj.icon = "https://cryptologos.cc/logos/xrp-xrp-logo.svg"
                        obj.save()

        except requests.RequestException as e:
            print(f"Error making API request: {e}")
        


@receiver(post_migrate)
def create_initial_instance(sender, **kwargs):
    if sender.name == 'crypto':
        if not DepositSettings.objects.exists():
            DepositSettings.objects.create(title="По умолчанию")

