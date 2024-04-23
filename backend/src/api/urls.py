from django.urls import path, include

urlpatterns = [
    path('authentication/', include('src.authentication.urls')),
    path('', include('src.users.urls')),
    path('', include('src.management.urls')),
    path('', include('src.notifications.urls')),
]
