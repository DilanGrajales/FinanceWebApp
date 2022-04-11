from django.urls import path, re_path
from .views import login_view, register_user
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password_reset/', PasswordResetView.as_view(), name="password_reset"),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), {
        'template_name': 'registration/password_reset_confirm.html'},name='password_reset_confirm'
    ),
    path('done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
