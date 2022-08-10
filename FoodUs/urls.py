from django import views
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]