import this
from django.urls import include, path, reverse_lazy
from django.contrib.auth.views import LoginView, logout_then_login

from generales.views import Home, HomeSinPrivilegios

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('accounts/login/', LoginView.as_view(template_name='generales/login.html'), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('sin_privilegios/', HomeSinPrivilegios.as_view(), name='sin_privilegios'),
    
]
