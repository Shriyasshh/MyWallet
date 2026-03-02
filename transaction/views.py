from django.shortcuts import render,redirect
from accounts.models import AddAccount
from transaction.models import Transaction
from django.contrib.auth.decorators import login_required
import decimal
# Create your views here.

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'transactions': transactions
    }
    return render(request, 'transactions.html',context)

@login_required
def add_record(request):
    
    acc = AddAccount.objects.filter(user=request.user)
    currency = acc.first().get_currency_display() if acc.exists() else ''

    if request.method == "POST":
        payment_type = request.POST.get('payment_type')
        amount_str = request.POST.get('amount')
        amount = decimal.Decimal(amount_str) if amount_str else decimal.Decimal('0')
        category = request.POST.get('category')
        account_id =request.POST.get('account') or request.POST.get('from_account')
        to_account_id = request.POST.get('to_account') or None
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        payee = request.POST.get('payee')
        print(payment_type, amount, category, account_id, to_account_id, date, time, note, payee)
        Transaction.objects.create(
            user=request.user,
            payment_type=payment_type,
            amount=amount,
            category=category,
            account_id=account_id,
            to_account_id=to_account_id,
            date=date,
            time=time,
            note=note,
            payee=payee,)

        return redirect('add_record')   # redirect after save

    context = {
        'acc': acc,
        'currency': currency,
    }

    return render(request, 'add_record.html', context)

def transaction(request,pk):
    account = AddAccount.objects.get(slug=pk, user=request.user)
    trans = Transaction.objects.filter(user=request.user,account=account).order_by('-date')
    context ={
        'account': account,
        'trans': trans
    }
    return render(request, 'transaction.html',context)