from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.http import HttpResponseRedirect

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
        messages.info(request, 'POST request received on the dashboard.')
        return redirect('dashboard')

# Logout Views
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return HttpResponseRedirect('/login/')
