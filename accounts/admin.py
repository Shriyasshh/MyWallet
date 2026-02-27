from django.contrib import admin
from .models import AddAccount

class AddAccountAdmin(admin.ModelAdmin):
    list_display = ('user','accountType','accountName','currency','accountBalance')
    search_fields = ('user',)

admin.site.register(AddAccount,AddAccountAdmin)