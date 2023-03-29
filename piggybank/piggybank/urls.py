from django.contrib import admin
from django.urls import path
from rest_framework import routers

from core import views

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryModelViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currencies/', views.CurrencyListAPIView.as_view(), name='currencies')
]

urlpatterns += router.urls
