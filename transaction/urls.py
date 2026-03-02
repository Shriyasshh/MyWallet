from django.urls import path
from . import views

urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('add-record/', views.add_record, name='add_record'),
    path('<slug:pk>',views.transaction,name = 'transaction'),
    
]
