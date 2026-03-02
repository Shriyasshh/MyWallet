from django.shortcuts import render,redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import AddAccount
from transaction.models import Transaction
from .forms import AddAccountForm
from django.template.defaultfilters import slugify


# Create your views here.

@login_required
def accounts(request):
    acc = AddAccount.objects.filter(user=request.user)
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0

    # attach recent transactions for each account (3 most recent)
    for a in acc:
        a.recent_txns = list(Transaction.objects.filter(user=request.user, account=a).order_by('-date', '-time')[:3])

    currency = acc.first().get_currency_display() if acc.exists() else ''
    context= {
        'acc': acc,
        'total_balance': total_balance,
        'currency': currency,
    }
    return render(request, 'accounts.html',context)

@login_required
def add_account(request):
    if request.method =='POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('accounts')
        else:
            form = AddAccountForm(request.POST)
    
    context = {'form': form}
    return render(request, 'add_account.html',context)