from django.urls import path
from django.contrib.auth import views as auth_views
from app.views.user.user_register_view import UserRegisterView
from app.views.user.user_logout_view import UserLogoutView

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(
        template_name="user/login.html",
        redirect_authenticated_user=True,
        next_page="/profile"
    ), name='login'),
    path("logout/", UserLogoutView.as_view(), name='logout'),
    path("register/", UserRegisterView.as_view(), name="register"),
]
