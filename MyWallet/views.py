from django.shortcuts import render
from accounts.models import AddAccount
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required
def home(request):
    # acc = AddAccount.objects.filter(user=request.user)
    acc = AddAccount.objects.all()
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    currency = acc.first().get_currency_display() if acc.exists() else ''
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]

    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
        'transactions': transactions
    }
    return render(request, 'home.html',context)
