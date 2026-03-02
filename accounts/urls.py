from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.accounts,name='accounts'),
    path('add-account/', views.add_account, name='add_account'),
    
    # TRANSACTIONS
    path('transactions/',include('transaction.urls')),
]
