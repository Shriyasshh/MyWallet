from django.urls import path
from . import views

urlpatterns = [
    path('',views.accounts,name='accounts'),
    path('add-account/', views.add_account, name='add_account'),
    
]
