from django.shortcuts import render
from accounts.models import AddAccount
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# @login_required
def home(request):
    # acc = AddAccount.objects.filter(user=request.user)
    acc = AddAccount.objects.all()
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    currency = acc.first().get_currency_display() if acc.exists() else ''
    print(currency)
    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
    }
    return render(request, 'home.html',context)

