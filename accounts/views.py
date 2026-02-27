from django.shortcuts import render,redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import AddAccount
from .forms import AddAccountForm

# Create your views here.

@login_required
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

@login_required
def add_account(request):
    form = AddAccountForm()
    if request.method =='POST':
        form = AddAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('accounts')
        else:
            print("Form errors:", form.errors)
    
    context = {'form': form}
    return render(request, 'add_account.html',context)