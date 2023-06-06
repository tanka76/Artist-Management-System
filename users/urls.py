
from django.urls import path
from .views import LoginView,UserCreateView,Dashboard

app_name="users"


urlpatterns = [

    path("", Dashboard.as_view(), name="dashboard"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("register/", UserCreateView.as_view(), name="register_view"),
    
]

