from django.db import models
from django.shortcuts import reverse
import random
# Create your models here.
class Crypto(models.Model):
    icon = models.URLField(max_length=1000, default="", verbose_name="Иконка")
    name = models.CharField(max_length=50, default="", verbose_name="Имя")
    symbol = models.CharField(max_length=10, default="", verbose_name="Индекс")
    price = models.DecimalField(max_digits=20, decimal_places=10, default=0, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="Включение/Выключение")
    
    def update_price(self, new_price):
        self.price = new_price


    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper() # Change "symbol" to uppercase before saving 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.symbol}"
    
    class Meta:
        verbose_name = "Монета"
        verbose_name_plural = "Монеты"

class Bank(models.Model):
    icon = models.URLField(max_length=1000, default="", verbose_name="Иконка")
    name = models.CharField(max_length=50, default="", verbose_name="Название")
    symbol = models.CharField(max_length=10, default="", verbose_name="Валюта")
    price = models.DecimalField(max_digits=20, decimal_places=3, default=0, verbose_name="Цена к доллару")
    reserve = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=round(random.uniform(500000, 3000000), 2),
        verbose_name="Резерв")
    is_available = models.BooleanField(default=True, verbose_name="Включение/Выключение")

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper() # Change "symbol" to uppercase before saving 
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.symbol}"
    
    class Meta:
        verbose_name = "Банк"
        verbose_name_plural = "Банки"

class DepositPayment(models.Model):
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, verbose_name="Монета")
    NETWOR_CHOISES = (
                ('', ''),
                ('TRC-20', 'TRC-20'),
                ('BEP-20', 'BEP-20'),
                ('ERC-20', 'ERC-20'),)
    network = models.CharField(max_length=100, verbose_name="Сеть", null=True, blank=True, default="", choices=NETWOR_CHOISES, help_text="Указывать только на монеты где нужно")
    qrcode = models.ImageField(upload_to="", verbose_name="QR-код")
    address = models.CharField(max_length=1000, verbose_name="Адрес")
    is_available = models.BooleanField(default=True, verbose_name="Включение/Выключение")


    def __str__(self):
        return f"{self.crypto.symbol}"
    
    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class DepositSettings(models.Model):
    @staticmethod
    def generate_crypto_choices():
        # Assume Crypto is a list of predefined cryptocurrencies
        crypto_choices = [(crypto, crypto) for crypto in Crypto] + [('RUB', 'RUB')]
        return crypto_choices

    title = models.CharField(max_length=100, editable=False, verbose_name="")
    crypto = models.CharField(max_length=20, verbose_name="Валюта")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10, verbose_name="min $", blank=True)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=100000, verbose_name="max $", blank=True)
    
    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        verbose_name = "Лимит"
        verbose_name_plural = "Лимиты"


class Exchange(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, verbose_name="ID")
    dep_wallet = models.CharField(max_length=500, null=True, verbose_name="Ваш адрес")
    coinFrom = models.CharField(max_length=100, null=True, verbose_name="")
    coinTo = models.CharField(max_length=100, null=True, verbose_name="")
    sumFrom = models.CharField(max_length=100, null=True, verbose_name="Из")
    sumTo = models.CharField(max_length=100, null=True, verbose_name="В")
    email = models.EmailField(verbose_name="Почта")
    wallet = models.CharField(max_length=500, null=True, verbose_name="Адрес")
    dateTime = models.DateTimeField(auto_now_add=True, verbose_name="Дата/Время")
    confirmed = models.BooleanField(default=False, verbose_name="Подтверждение")
    fio = models.CharField(max_length=500, null=True, verbose_name="ФИО")
    
    PAYED = 'P'
    NOT_PAYED = 'NP'
    WAIT = "W"
    
    STATUS_CHOICES = [
            (PAYED, 'Оплачено'),
            (NOT_PAYED, 'Не оплачено'),
            (WAIT, "В ожидании")
        ]
    status = models.CharField(max_length=30, verbose_name="Статус", choices=STATUS_CHOICES, default=WAIT)
    
    def __str__(self):
        return f"Обмен - {self.id}"
    
    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"