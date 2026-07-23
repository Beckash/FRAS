from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('facial_recognition_based__attendance_system_app.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
