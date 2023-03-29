from rest_framework.serializers import ModelSerializer

from core.views import CurrencyListAPIView


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = CurrencyListAPIView
        fields = ("id", "code", "name")
