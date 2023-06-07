from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,CreateView,TemplateView
from .forms import LoginForm,UserCreateForm,CustomLoginForm
from users.permissions import IsLoggedInMixin


# Create your views here.

class Dashboard(IsLoggedInMixin, TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def logout_user(request):
    logout(request)
    return redirect(reverse_lazy("users:login_view"))

class LoginView(View):
    template_name = "registration/login.html"
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:dashboard')
        else:
            error_message = 'Invalid email or password'  
            return render(request, self.template_name, {'error_message': error_message})
        
        

class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("users:login_view")


    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        email=form.cleaned_data.get("email")
        form.instance.username=email
        form.instance.is_staff=True
        form.instance.is_superuser=True
        user.password = make_password(password)
        user.save()        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)