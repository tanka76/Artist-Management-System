from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView,CreateView,TemplateView,UpdateView
from .forms import LoginForm,UserRegisterForm,CustomLoginForm,UserCreateForm,UserUpdateForm
from users.permissions import IsLoggedInMixin
from .models import AuthUser


# Create your views here.


class UserMixin(IsLoggedInMixin):
    model = AuthUser
    paginate_by = 10
    queryset = AuthUser.objects.filter(is_deleted=False)
    success_url = reverse_lazy("users:dashboard")

class Dashboard(IsLoggedInMixin, TemplateView):
    template_name = "user_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users']=AuthUser.objects.all()
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
        
    
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
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
    

class UserCreateView(UserMixin, CreateView):
    form_class = UserCreateForm
    template_name = "user_create.html"

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
        print("Erroor============",form.errors)
        return super().form_invalid(form)
    

class UserUpdateView(UserMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "update.html"