from django.contrib import admin
from .models import Transaction
# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user','payment_type','amount',)
admin.site.register(Transaction,TransactionsAdmin)