from django.shortcuts import render
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import AddAccount

# Create your views here.

# @login_required
def accounts(request):
    # acc = AddAccount.objects.filter(user=request.user)
    acc = AddAccount.objects.all()
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    currency = acc.first().get_currency_display() if acc.exists() else ''
    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
    }
    return render(request, 'accounts.html',context)

def add_account(request):
    return render(request, 'add_account.html')