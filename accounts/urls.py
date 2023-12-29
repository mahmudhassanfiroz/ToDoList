
from django.urls import path
from .views import SignUpView, LoginView, DashboardView, LogoutView, BaseView, activity_list, notification_list, mark_notification_as_read

app_name = 'accounts' 

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),    
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('password_reset/', UserChangePasswordView.as_view(), name='password_reset'), 
    
    path('', BaseView.as_view(), name='base_view'),  # Assuming you want the BaseView to be used for the base URL
    path('activities/', activity_list, name='activity_list'),
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark_as_read/', mark_notification_as_read, name='mark_notification_as_read'),
    
]

