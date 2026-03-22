# from django.utils import timezone
from datetime import date,timedelta
from django.shortcuts import render,redirect
from django.urls import reverse
from accounts.models import AddAccount
from transaction.models import Transaction , Debt
from django.contrib.auth.decorators import login_required
import decimal
from django.db.models import Q
from django.core.paginator import Paginator
from transaction.forms import DebtForm
from django.db.models import Sum

# Create your views here.

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    accounts= AddAccount.objects.filter(user=request.user)

    # Filters
    date_filter = request.GET.get('date')
    category = request.GET.get('category')
    account_id = request.GET.get('account')
    payment_type = request.GET.get('type')
    search = request.GET.get('search')

    
    if category:
        transactions = transactions.filter(category=category)

    # Filter by account if selected
    if account_id:        
        try:
            account = AddAccount.objects.get(id=account_id, user=request.user)
            transactions = transactions.filter(account=account)
        except AddAccount.DoesNotExist:
            pass

    if payment_type:
        transactions = transactions.filter(payment_type=payment_type)

    today = date.today()

    if date_filter == "month":
        transactions = transactions.filter(date__month=today.month)
    elif date_filter == "7days":
        transactions = transactions.filter(date__gte=today - timedelta(days=7))
    elif date_filter == "30days":
        transactions = transactions.filter(date__gte=today - timedelta(days=30))
    elif date_filter == "3months":
        transactions = transactions.filter(date__gte=today - timedelta(days=90))
    elif date_filter == "year":
        transactions = transactions.filter(date__year=today.year)
    
    if search:
        transactions = transactions.filter(Q(note__icontains=search) |Q(payee__icontains=search)
        )

    paginator = Paginator(transactions, 15)   # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'accounts': accounts,
        'transactions': transactions,
        'categories': Transaction.CATEGORY_CHOICES,
        'selected_date': date_filter,
        'selected_category': category,
        'selected_account': account_id,
        'selected_type': payment_type,
        'search_query': search,
        'page_obj': page_obj,
        'total_records': paginator.count,
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

@login_required
def transaction(request,pk):
    account = AddAccount.objects.get(slug=pk, user=request.user)
    transactions = Transaction.objects.filter(user=request.user,account=account).order_by('-date')
    accounts= AddAccount.objects.filter(user=request.user)

    date_filter = request.GET.get('date')
    category = request.GET.get('category')
    account_id = request.GET.get('account')
    payment_type = request.GET.get('type')
    search = request.GET.get('search')

    
    if category:
        transactions = transactions.filter(category=category)

    if payment_type:
        transactions = transactions.filter(payment_type=payment_type)

    today = date.today()

    if date_filter == "month":
        transactions = transactions.filter(date__month=today.month)
    elif date_filter == "7days":
        transactions = transactions.filter(date__gte=today - timedelta(days=7))
    elif date_filter == "30days":
        transactions = transactions.filter(date__gte=today - timedelta(days=30))
    elif date_filter == "3months":
        transactions = transactions.filter(date__gte=today - timedelta(days=90))
    elif date_filter == "year":
        transactions = transactions.filter(date__year=today.year)
    
    if search:
        transactions = transactions.filter(Q(note__icontains=search) |Q(payee__icontains=search)
        ) 
    
    # Pagination
    paginator = Paginator(transactions, 15)   # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        # For tractions display from which account
        'account': account,
        # For filter bar
        'accounts': accounts,
        'transactions': transactions,
        'categories': Transaction.CATEGORY_CHOICES,
        'selected_date': date_filter,
        'selected_category': category,
        'selected_account': account_id,
        'selected_type': payment_type,
        'search_query': search,
        'page_obj': page_obj,
        'total_records': paginator.count,
    }
    return render(request, 'transaction.html',context)

@login_required
def debt_manager(request):
    acc = AddAccount.objects.filter(user=request.user)
    currency = acc.first().get_currency_display() if acc.exists() else ''
    print(currency)
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
    # Net Worth
    net_worth = lent - borrowed
    
    debt = Debt.objects.filter(user=request.user)
    today = date.today()
    for d in debt:
        d.paid_percentage = (d.returned * 100) / d.amount
        d.remain = d.amount - d.returned
        if d.paid_percentage == 100:
            d.status = "Settled"
            d.status_class = "settled"
        elif today > d.duedate:
            d.status = "Overdue"
            d.status_class = "overdue"
        elif 0 <= (d.duedate - today).days <= 7:
            d.status = "Upcoming"
            d.status_class = "upcoming"
        else:
            d.status = "On Track"
            d.status_class = "ok"
        print(d.remain)
    if request.method =='POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.user = request.user
            # first persist the debt so its balance update applies
            debt.save()
            
            return redirect('debt-manager')
    else:
        form = DebtForm()
    
    context = {'form': form,
               'acc': acc,
               'currency': currency,
               'borrowed': borrowed,
               'lent': lent,
               'borrowed_count': borrowed_count,
               'lent_count': lent_count,
               'net_worth': net_worth,
               'debt': debt,
               }
    return render(request, 'debt-manager.html',context)


@login_required
def settle_debt(request):
    if request.method != 'POST':
        return redirect('debt-manager')

    debt_id = request.POST.get('debt_id')
    amount_str = request.POST.get('partial_amount')
    payment_date = request.POST.get('payment_date')
    note = request.POST.get('note', '').strip()

    try:
        debt = Debt.objects.get(id=debt_id, user=request.user)
    except Debt.DoesNotExist:
        return redirect('debt-manager')

    try:
        payment_amount = decimal.Decimal(amount_str or '0')
    except (decimal.InvalidOperation, TypeError):
        payment_amount = decimal.Decimal('0')

    if payment_amount <= 0:
        return redirect('debt-manager')

    remaining = debt.amount - debt.returned
    if payment_amount > remaining:
        payment_amount = remaining

    # Adjust linked account balance depending on debt type
    account = debt.linkedAccount
    if debt.debtType == 'borrowed':
        # User is paying back money => money leaves the account
        account.accountBalance -= payment_amount
    else:
        # User is receiving money => money enters the account
        account.accountBalance += payment_amount
    account.save()

    debt.returned += payment_amount
        
    debt.save()

    # Create a matching Transaction record for the repayment
    transaction_type = 'expense' if debt.debtType == 'borrowed' else 'income'
    Transaction.objects.create(
        user=request.user,
        payment_type=transaction_type,
        amount=payment_amount,
        category=debt.debtType,
        account=account,
        date=payment_date or debt.date,
        time='12:00',
        payee=debt.borrow_lent_from,
        note=note or f"Payment towards {debt.debtType} debt",
    )

    return redirect('debt-manager')
