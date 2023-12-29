from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from .models import Activity, Notification
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

# Sign Up Views
class SignUpView(FormView):
  form_class = SignUpForm
  success_url = '/login/'
  template_name = 'accounts/signup.html'

  def form_valid(self, form):
    form.save()
    messages.success(self.request, 'Account created successfully')
    return super().form_valid(form)

# Login Views
class LoginView(FormView):
  form_class = AuthenticationForm
  template_name = 'accounts/login.html'
  success_url = '/dashboard/'

  def form_valid(self, form):
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
      login(self.request, user)
      messages.success(self.request, 'You are now logged in')
    return super().form_valid(form)

# Dashboard Views

class DashboardView(View):
  template_name = 'accounts/dashboard.html'
    
  def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      return redirect('login')
    return super().dispatch(request, *args, **kwargs)

  def get(self, request, *args, **kwargs):
    tasks = self.request.user.tasks.all()
    context = {'tasks': tasks}
    return render(request, self.template_name, context)

  def post(self, request, *args, **kwargs):
    # Handle POST requests here if needed
    messages.info(request, 'POST request received on the dashboard.')
    return redirect('dashboard') 


# Logout Views
class LogoutView(View):
  def get(self, request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect('/login/')
  
# Change password without old password 
# class UserChangePasswordView(PasswordChangeView):
#     template_name = 'accounts/change_password.html'
#     success_url = '/dashboard/'

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, 'Password changed successfully!')
#         update_session_auth_hash(self.request, self.request.user)
#         return response

#     def form_invalid(self, form):
#         messages.error(self.request, 'Failed to change password. Please correct the errors below.')
#         return super().form_invalid(form)

#     def get(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('login')
#         return super().get(request, *args, **kwargs) 

class BaseView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, 'base.html', context)

@login_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user)
    return render(request, 'accounts/activity_list.html', {'activities': activities})

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'accounts/notification_list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

