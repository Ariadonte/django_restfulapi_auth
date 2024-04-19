from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import RegisterView, LoginView, UserView, LogoutView, RefreshView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', RefreshView.as_view())
]
