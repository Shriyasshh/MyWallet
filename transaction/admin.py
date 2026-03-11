from django.contrib import admin
from .models import Transaction,Debt
# Register your models here.

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('user','payment_type','amount',)
admin.site.register(Transaction,TransactionsAdmin)

class DebtAdmin(admin.ModelAdmin):
    list_display =('user','debtType','amount','borrow_lent_from','duedate','repayment')
admin.site.register(Debt,DebtAdmin)
