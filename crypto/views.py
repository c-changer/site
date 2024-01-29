from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Crypto, DepositPayment, DepositSettings, Exchange, Bank
from decimal import Decimal

import random

import secrets

# Create your views here.
def home(request):
    exchange_id = request.COOKIES.get('exchange_id')
    
    if exchange_id:
        return redirect('deal')
    
    payments = DepositPayment.objects.filter(is_available=True)
    deposit = DepositPayment.objects.filter(is_available=True)
    settings = DepositSettings.objects.get(title="Настройки депозита")
    banks = Bank.objects.filter(is_available=True)
    
    for dep in deposit:
        dep.crypto.price -= dep.crypto.price * Decimal(0.025)
        dep.crypto.save(commit=False)

    try:
        obj = Crypto.objects.get(symbol="BTC",is_available=True)
        default_payment = DepositPayment.objects.filter(crypto=obj, is_available=True).first()
    except Exception as e:
        default_payment = payments[0]
        
    try:
        obj = Crypto.objects.get(symbol="USDT")
        default_dep = DepositPayment.objects.filter(crypto=obj, is_available=True).first()
    except Exception as e:
        default_dep = deposit[0]
        
    try:
        if default_payment == default_dep:
            default_dep = deposit[1]
    except Exception as e:
        pass
        
    price_ratio = default_payment.crypto.price -  default_payment.crypto.price * Decimal(0.025)

    min_amount_payment = round(settings.min_amount / default_payment.crypto.price, 5)
    max_amount_payment = round(settings.max_amount / default_payment.crypto.price, 5)
    
    if default_dep.crypto.symbol == "USDT":
        min_amount_dep = settings.min_amount
        max_amount_dep = settings.max_amount
    else:
        min_amount_dep = round(settings.min_amount / default_dep.crypto.price, 5)
        max_amount_dep = round(settings.max_amount / default_dep.crypto.price, 5)
    
    reserve = settings.max_amount / settings.min_amount * Decimal(25.2716)
    context = {
        "payments": payments,
        "deposit": deposit,
        "banks": banks,
        "settings": settings,
        "default_payment": default_payment,
        "default_dep": default_dep,
        "price_ratio": round(price_ratio, 2),
        "min_amount_dep": min_amount_dep,
        "max_amount_dep": max_amount_dep,
        "min_amount_payment": min_amount_payment,
        "max_amount_payment": max_amount_payment,
        "reserve": round(reserve, 2),
    }

    return render(request, "crypto/home.html", context)

def exchange(request):
    try:
        if request.method == 'POST':
            coinFrom = request.POST.get('symbolFromInput')
            coinTo = request.POST.get('symbolToInput')
            sumFrom = request.POST.get('sumFrom')
            sumTo = request.POST.get('sumTo')
            priceFrom = request.POST.get('priceFromInput').replace(',', '.')
            priceTo = request.POST.get('priceToInput').replace(',', '.')
            email = request.POST.get('email')
            wallet = request.POST.get('wallet')
            
            try:
                fio = request.POST.get('fio')
            except:
                pass

            settings = DepositSettings.objects.get(title="Настройки депозита")
            minAmount = settings.min_amount
            maxAmount = settings.max_amount
            
            if Decimal(sumFrom) < (Decimal(minAmount) / Decimal(priceFrom)) or Decimal(sumFrom) > (Decimal(maxAmount) / Decimal(priceFrom)) or Decimal(sumTo) < (Decimal(minAmount) / Decimal(priceTo)) or Decimal(sumTo) > (Decimal(maxAmount) / Decimal(priceTo)):
                response_data = {'success': False, 'input': ['sumFrom', 'sumTo']}
                return JsonResponse(response_data)
            
            exchange_id = secrets.token_hex(6)  # 6 bytes will generate 12 characters
            
            first_word = coinFrom.split()[0]
            
            try:
                crypto = Crypto.objects.get(name=first_word)
            except:
                crypto = Crypto.objects.get(symbol=first_word)
            
            deposit_payment = DepositPayment.objects.get(crypto=crypto)    
            
            exchange = Exchange.objects.create(
                id=exchange_id,
                coinFrom=coinFrom,
                coinTo=coinTo,
                sumFrom=sumFrom,
                sumTo=sumTo,
                email=email,
                wallet=wallet,
                dep_wallet=deposit_payment.address,
                fio=fio
            )
            
            exchange.save()
            
            # Set the 12-character token as a cookie
            response = redirect('deal')
            response.set_cookie('exchange_id', exchange_id, 3600)

            return response
            # return redirect('contact')
        else:
            response_data = {'success': False, 'message': 'Метод запроса не поддерживается'}
            return JsonResponse(response_data)
    except Exception as e:
        print(e)  # Print the exception to the console for debugging
        response_data = {'success': False, 'message': e}
        return JsonResponse(response_data)
    
def deal(request):
    # Retrieve the exchange_id from the cookie
    exchange_id = request.COOKIES.get('exchange_id')

    if exchange_id:
        exchange = Exchange.objects.get(id=exchange_id)
        
        context = {
            'exchange': exchange
        }
        
        return render(request, 'crypto/deal.html', context)
    else:
        # Handle the case where exchange_id is not found in the cookie
        return redirect("home")

def confirm(request):
    exchange_id = request.COOKIES.get('exchange_id')
    if exchange_id:
        exchange = Exchange.objects.get(id=exchange_id)
        exchange.confirmed = True
        exchange.save()
        
        # try:
        #     htmly = get_template('email.html')
        #     context = {
        #         "exchange": exchange
        #     }
        #     subject = f'Order {exchange.id}'
        #     from_email = f'c-changer.in <{settings.EMAIL_HOST_USER}>'
        #     to_email = user.email
        #     html_content = htmly.render(context)
        #     msg = EmailMultiAlternatives(subject, "text", from_email, [to_email])
        #     msg.attach_alternative(html_content, "text/html")

        #     msg.send()
        # except:
        #     None
        
        return redirect('deal')
    return redirect('deal')

def cancel(request):
    try:
        # Retrieve the exchange_id from the cookie
        exchange_id = request.COOKIES.get('exchange_id')

        if exchange_id:
            # Delete the exchange record with the specified ID
            Exchange.objects.filter(id=exchange_id).delete()

            # Delete the exchange_id cookie
            response = redirect('home')  # Redirect to the home page (adjust the URL as needed)
            response.delete_cookie('exchange_id')

            return response
        else:
            # Handle the case where exchange_id is not found in the cookie
            return render(request, 'crypto/error.html', {'message': 'Invalid session'})
    except Exception as e:
        print(e)  # Print the exception to the console for debugging
        response_data = {'success': False, 'message': 'Internal Server Error'}
        return JsonResponse(response_data)


def error(request):
    exchange_id = request.COOKIES.get('exchange_id')
    
    if exchange_id:
        exchange = Exchange.objects.get(id=exchange_id)
        
        context = {
            'exchange': exchange
        }
        
        # try:
        #     htmly = get_template('error.html')
        #     context = {
        #         "exchange": exchange
        #     }
        #     subject = f'Order {exchange.id}'
        #     from_email = f'c-changer.in <{settings.EMAIL_HOST_USER}>'
        #     to_email = user.email
        #     html_content = htmly.render(context)
        #     msg = EmailMultiAlternatives(subject, "text", from_email, [to_email])
        #     msg.attach_alternative(html_content, "text/html")

        #     msg.send()
        # except:
        #     None

        response = render(request, "crypto/error.html", context)
        response.delete_cookie('exchange_id')
        return response
    return redirect("home")

def success(request):
    exchange_id = request.COOKIES.get('exchange_id')
    
    if exchange_id:
        exchange = Exchange.objects.get(id=exchange_id)
        
        context = {
            'exchange': exchange
        }

        # try:
        #     htmly = get_template('success.html')
        #     context = {
        #         "exchange": exchange
        #     }
        #     subject = f'Order {exchange.id}'
        #     from_email = f'c-changer.in <{settings.EMAIL_HOST_USER}>'
        #     to_email = user.email
        #     html_content = htmly.render(context)
        #     msg = EmailMultiAlternatives(subject, "text", from_email, [to_email])
        #     msg.attach_alternative(html_content, "text/html")

        #     msg.send()
        # except:
        #     None
            
        response = render(request, "crypto/success.html", context)
        response.delete_cookie('exchange_id')
        return response
    return redirect("home")

def check_status(request):
    exchange_id = request.COOKIES.get('exchange_id')
    
    if exchange_id:
        exchange = Exchange.objects.get(id=exchange_id)
        return JsonResponse({"status": exchange.status})