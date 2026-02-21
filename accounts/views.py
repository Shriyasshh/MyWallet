from django.shortcuts import render

# Create your views here.
def add_account(request):
    return render(request, 'add_account.html')