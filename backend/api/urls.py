from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('upload/', views.upload_file, name='upload_file')
]
