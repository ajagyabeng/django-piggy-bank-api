from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, TransactionSerializer, ReadTransactionSerializer, WriteTransactionSerializer


class CurrencyListAPIView(ListAPIView):
    """
    ListApiView: Handles get requests only.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None


class TransactionModelViewSet(ModelViewSet):
    """When using a foreign key, tell django to pre-fetch them(select_related) prior to a query. It makes it faster"""
    # queryset = Transaction.objects.all()
    queryset = Transaction.objects.select_related("currency", "category")

    # FILTER
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["description"]
    ordering_fields = ["amount"]
    filterset_fields = ["currency__code"]

    def get_serializer_class(self):
        """ModelViewSet adds all the actions(List, Create, Retrieve, Update, Destroy) on the view"""
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer
