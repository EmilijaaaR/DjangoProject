from django.urls import path
from .views.views import RegisterView, LoginView
from .views.password_reset_views import CustomPasswordResetView, CustomPasswordResetConfirmView
from .views.views import UserProfileUpdateView
from .views.views import UserDeactivateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
]