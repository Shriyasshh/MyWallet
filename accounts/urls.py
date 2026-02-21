from django.urls import path
from . import views

urlpatterns = [
    path('add-account/', views.add_account, name='add_account'),
    
]
