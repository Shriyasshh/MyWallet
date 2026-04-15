from django.shortcuts import render,redirect
from accounts.models import AddAccount
from transaction.models import Transaction,Debt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date, timedelta
from .forms import SignInForm
# from django.utils import timezone
# from collections import defaultdict
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import auth
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.hashers import check_password




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
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)
            if AddAccount.objects.filter(user=request.user).count() > 0:
                return redirect('home')
            return redirect('add_account')
    else:
        login_form = AuthenticationForm()
    context={
        'l_form':login_form
    }
    return render(request, 'login.html',context)

def signin(request):
    if request.method =='POST':
        sign_form =SignInForm(request.POST)
        if sign_form.is_valid():
            sign_form.save()
            return redirect('login')
    else:    
        sign_form =SignInForm()

    context={
    's_form':sign_form,
    }
    return render(request, 'signin.html',context)

def logout(request):
    auth_logout(request)
    return redirect('landing')

def landing(request):
    return render(request, 'landing.html')


# @login_required
# def settings(request):
#     return render(request, 'setting.html')

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         user = request.user
#         user.first_name = request.POST.get('first_name', '')
#         user.last_name  = request.POST.get('last_name', '')
#         user.save()
#     messages.success(request, 'Profile updated successfully.')
#     return redirect('settings')

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         current  = request.POST.get('current_password')
#         new_pass = request.POST.get('new_password')
#         confirm  = request.POST.get('confirm_password')

#         if not request.user.check_password(current):
#             messages.error(request, 'Current password is incorrect.')
#             return redirect('settings')

#         if new_pass != confirm:
#             messages.error(request, 'Passwords do not match.')
#             return redirect('settings')

#         # Update in Django
#         request.user.set_password(new_pass)
#         request.user.save()
#         update_session_auth_hash(request, request.user)  # keep user logged in

#         # Also update in Supabase Auth if using Supabase auth
#         # supabase.auth.update_user({'password': new_pass})

#         messages.success(request, 'Password updated successfully.')
#     return redirect('settings')