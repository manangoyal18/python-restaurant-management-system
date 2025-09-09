from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path('signup/', views.UserRegistrationView.as_view(), name='user-signup'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token-refresh'),
    
    # User management endpoints (public)
    path('users/', views.get_all_users, name='get-users'),
    path('users/<str:user_id>/', views.get_user, name='get-user'),
    
    # User profile endpoints (authenticated)
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]