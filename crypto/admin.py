from django.contrib import admin
from .models import Crypto, Bank, DepositPayment, DepositSettings, Exchange

# Register your models here.
class CryptoAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False    
    list_display = ['name', 'symbol', 'is_available']
    list_editable = ['is_available']
    
admin.site.register(Crypto, CryptoAdmin)

class BankAdmin(admin.ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False    
    list_display = ['name', 'symbol', 'price', 'reserve', 'is_available']
    list_editable = ['price', 'reserve', 'is_available']
    
admin.site.register(Bank, BankAdmin)

class DepositCryptoAdmin(admin.ModelAdmin):
    # actions_on_top = False
    actions_on_bottom = False    
    list_display = ['crypto', 'address', 'network', 'is_available']
    list_editable = ['address', 'is_available']

admin.site.register(DepositPayment, DepositCryptoAdmin)

class DepositSettingsAdmin(admin.ModelAdmin):
    actions_on_top = False
    actions_on_bottom = False    
    list_display = ['title', 'min_amount', 'max_amount']
    list_editable = ['min_amount', 'max_amount']

    def has_add_permission(self, request):
        # Disable the ability to add new instances
        return False
    
admin.site.register(DepositSettings, DepositSettingsAdmin)

class ExchangeAdmin(admin.ModelAdmin):
    actions_on_bottom = False    
    list_display = ['id', 'status', 'sumFrom', 'coinFrom', 'sumTo', 'coinTo', 'wallet', 'dateTime', ]
    list_editable = ["status"]
    ordering = ['-dateTime']
    def has_add_permission(self, request):
        # Disable the ability to add new instances
        return False

admin.site.register(Exchange, ExchangeAdmin)