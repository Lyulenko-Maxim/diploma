from django.urls import path, include

from .views import (
    ActivateView,
    LoginView,
    LogoutView,
    RegisterView,
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('activate/<str:token>/', ActivateView.as_view()),
]
