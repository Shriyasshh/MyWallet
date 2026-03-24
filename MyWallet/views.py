from django.shortcuts import render
from accounts.models import AddAccount
from transaction.models import Transaction,Debt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date ,timedelta

@login_required
def home(request):
    acc = AddAccount.objects.filter(user=request.user)
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    currency = acc.first().get_currency_display() if acc.exists() else ''
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:10]
    # total_debt = Debt.objects.filter(user=request.user).aggregate(total = Sum('returned'))['total'] or 0
    # print(total_debt)
    today = date.today()
    dates = str(today.strftime('%A, %b %d,%Y'))
    
    # Last 30 days
    # income = Transaction.objects.filter(user=request.user,payment_type='income',date__gte= today - timedelta(days=30)).aggregate(total = Sum('amount'))['total'] or 0
    # expense = Transaction.objects.filter(user=request.user,payment_type='expense',date__gte= today - timedelta(days=30)).aggregate(total = Sum('amount'))['total'] or 0
    # trans_count = Transaction.objects.filter(user=request.user,payment_type='expense',date__gte= today - timedelta(days=30)).count()
    
    # Current Month
    income = Transaction.objects.filter(user=request.user,payment_type='income',date__month=today.month).aggregate(total = Sum('amount'))['total'] or 0
    expense = Transaction.objects.filter(user=request.user,payment_type='expense',date__month=today.month).aggregate(total = Sum('amount'))['total'] or 0
    trans_count = Transaction.objects.filter(user=request.user,payment_type__in=['expense', 'borrowed', 'lent'],date__month=today.month).count()

    # Month
    month = today.strftime('%b')
    year = today.strftime('%Y')

    debt_borrowed = Debt.objects.filter(user=request.user, debtType = 'borrowed')
    borrowed_amt = debt_borrowed.aggregate(total = Sum('amount'))['total'] or 0
    borrowed_ret = debt_borrowed.aggregate(total = Sum('returned'))['total'] or 0
    borrowed = borrowed_amt - borrowed_ret
    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
        'transactions': transactions,
        'date': dates,
        'income': income,
        'expense': expense,
        # 'savings': savings,
        'trans_count': trans_count,
        'month': month,
        'year': year,
        'debt': borrowed,
    }
    return render(request, 'home.html',context)


def login(request):
    return render(request, 'login.html')

def landing(request):
    return render(request, 'landing.html')