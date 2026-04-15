"""
URL configuration for MyWallet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('accounts/',include('accounts.urls')),
    path('login/',views.login,name='login'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
    # path('report/',views.report,name='report'),
    # path('settings/',views.settings,name='settings'),
    # path('settings/profile/', views.update_profile, name='update_profile'),
    # path('settings/password/', views.change_password, name='change_password'),

]
