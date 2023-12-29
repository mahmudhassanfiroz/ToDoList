
from django.urls import path
from .views import SignUpView, LoginView, DashboardView, LogoutView
from django.contrib.auth import views as auth_views

app_name = 'accounts' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),  
    path('dashboard/', DashboardView.as_view(), name='dashboard'),    
    path('logout/', LogoutView.as_view(), name='logout'),
   
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]

