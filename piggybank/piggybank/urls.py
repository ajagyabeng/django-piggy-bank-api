from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from core import views

router = routers.SimpleRouter()
router.register(r'categories', views.CategoryModelViewSet, basename='category')
router.register(r'transactions', views.TransactionModelViewSet,
                basename='transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currencies/', views.CurrencyListAPIView.as_view(), name='currencies'),
    path('', include(router.urls))
]

# urlpatterns += router.urls
