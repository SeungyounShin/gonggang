from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('gonggang/', include('gonggang.urls')),
    path('admin/', admin.site.urls),
]
