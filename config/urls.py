from django.contrib import admin
from django.urls import path, include

from roulette import views
from roulette.views import home  # Dodany import

urlpatterns = [
    path('', home, name='home'),  # Dodana ścieżka dla strony głównej
    path('admin/', admin.site.urls),
    path('api/', include('roulette.urls')),
    path('api/check-auth/', views.check_auth, name='check-auth')
]