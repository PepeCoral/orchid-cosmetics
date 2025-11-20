from django.urls import path
from django.contrib.auth import views as auth_views
from app.views.user.user_register_view import UserRegisterView
from app.views.user.user_logout_view import UserLogoutView
from app.views.user.user_login_view import UserLoginView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path("register/", UserRegisterView.as_view(), name="register"),
]
