from django.shortcuts import render,redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import AddAccount
from transaction.models import Transaction,Debt
from .forms import AddAccountForm
from django.template.defaultfilters import slugify


# Create your views here.

@login_required
def accounts(request):
    acc = AddAccount.objects.filter(user=request.user)
    total_balance = acc.aggregate(total = Sum('accountBalance'))['total'] or 0
    acc_count = acc.count()
    

    # attach recent transactions for each account (3 most recent)
    for a in acc:
        a.recent_txns = list(Transaction.objects.filter(user=request.user, account=a).order_by('-date', '-time')[:3])

    # Borrowed
    debt_borrowed = Debt.objects.filter(user=request.user, debtType = 'borrowed')
    borrowed_count = debt_borrowed.count()
    borrowed_amt = debt_borrowed.aggregate(total = Sum('amount'))['total'] or 0
    borrowed_ret = debt_borrowed.aggregate(total = Sum('returned'))['total'] or 0
    borrowed = borrowed_amt - borrowed_ret
    # Lent
    debt_lent = Debt.objects.filter(user=request.user, debtType = 'lent')
    lent_amt = debt_lent.aggregate(total = Sum('amount'))['total'] or 0
    lent_ret = debt_lent.aggregate(total = Sum('returned'))['total'] or 0
    lent = lent_amt - lent_ret
    lent_count = debt_lent.count()


    currency = acc.first().get_currency_display() if acc.exists() else ''
    context= {
        'acc': acc,
        'acc_count': acc_count,
        'total_balance': total_balance,
        'currency': currency,
        'borrowed': borrowed,
        'borrowed_count': borrowed_count,
        'lent': lent,
        'lent_count': lent_count,
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
        form = AddAccountForm()
    
    acc = AddAccount.objects.filter(user=request.user)
    
    context={
                'form': form,
                'acc': acc,
            }
    return render(request, 'add_account.html',context)