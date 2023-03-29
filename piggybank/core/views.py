from rest_framework.generics import ListAPIView

from core.models import Currency
from core.serializers import CurrencySerializer


class CurrencyListAPIView(ListAPIView):
    """
    ListApiView: Handles get requests only.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
