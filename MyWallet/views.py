from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def add_account(request):
    return render(request, 'add_account.html')