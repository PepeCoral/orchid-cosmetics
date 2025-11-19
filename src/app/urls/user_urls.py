from django.urls import path
from app.views.user.user_profile_view import UserProfileView
from app.views.user.user_update_view import UpdateUserView
from app.views.user.user_delete_view import DeleteUserView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('user/update/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('user/delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
]
