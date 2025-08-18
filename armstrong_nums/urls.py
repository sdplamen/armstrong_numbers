from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from armstrong_nums import views

urlpatterns = [
    path('', views.armstrong_numbers_view, name='index'),
    path('api/armstrong_numbers/', views.ArmstrongNumbersAPIView.as_view(), name='armstrong_numbers_api'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]