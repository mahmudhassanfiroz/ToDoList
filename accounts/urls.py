
from django.urls import path
from .views import SignUpView, LoginView, DashboardView, LogoutView

app_name = 'accounts' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),    
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('password_reset/', UserChangePasswordView.as_view(), name='password_reset'), 
]

