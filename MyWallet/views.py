from django.shortcuts import render
from accounts.models import AddAccount
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date ,timedelta

@login_required
def home(request):
    # acc = AddAccount.objects.filter(user=request.user)
    acc = AddAccount.objects.all()
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    currency = acc.first().get_currency_display() if acc.exists() else ''
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]

    today = date.today()
    dates = str(today.strftime('%A, %b %d,%Y'))
    
    # Last 30 days
    # income = Transaction.objects.filter(payment_type='income',date__gte= today - timedelta(days=30)).aggregate(total = Sum('amount'))['total'] or 0
    # expense = Transaction.objects.filter(payment_type='expense',date__gte= today - timedelta(days=30)).aggregate(total = Sum('amount'))['total'] or 0
    # trans_count = Transaction.objects.filter(payment_type='expense',date__gte= today - timedelta(days=30)).count()
    
    # Current Month
    income = Transaction.objects.filter(payment_type='income',date__month=today.month).aggregate(total = Sum('amount'))['total'] or 0
    expense = Transaction.objects.filter(payment_type='expense',date__month=today.month).aggregate(total = Sum('amount'))['total'] or 0
    trans_count = Transaction.objects.filter(payment_type='expense',date__month=today.month).count()

    # savings
    if income == 0 and expense == 0 and income <= expense:
        savings = 0
    else:
        savings = (income - expense)/income*100
        savings = str(round(savings, 2))

    # Month
    month = today.strftime('%b')
    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
        'transactions': transactions,
        'date': dates,
        'income': income,
        'expense': expense,
        'savings': savings,
        'trans_count': trans_count,
        'month': month
    }
    return render(request, 'home.html',context)
