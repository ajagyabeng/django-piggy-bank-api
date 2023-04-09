from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_xml.renderers import XMLRenderer

from .models import Currency, Category, Transaction
from .serializers import CurrencySerializer, CategorySerializer, ReadTransactionSerializer, WriteTransactionSerializer, ReportEntrySerializer, ReportParamsSerializer
from .reports import transaction_report


class CurrencyListAPIView(ListAPIView):
    """
    ListApiView: Handles get requests only.
    """
    permission_classes = [AllowAny]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    pagination_class = None
    # Make currency be rendered as an xml format. When set like this, no other format specified in the request that isnt in the renderer_classes will work.
    # renderer_classes = [XMLRenderer]


class CategoryModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # permission class has been set globally in settings.py hence there is no need to add it to the individual views.
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]

    # FILTER
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["description"]
    ordering_fields = ["amount"]
    filterset_fields = ["currency__code"]

    def get_queryset(self):
        """
        Returns items specific to only the user making the request.
        Pre-fetches the foreign key objects when the app starts running prior to a request. It increases the speed of the request.
        """
        return Transaction.objects.select_related(
            "currency", "category", "user").filter(user=self.request.user)

    def get_serializer_class(self):
        """ModelViewSet adds all the actions(List, Create, Retrieve, Update, Destroy) on the view"""
        if self.action in ("list", "retrieve"):
            return ReadTransactionSerializer
        return WriteTransactionSerializer


class TransactionReportAPIView(APIView):
    """Add view url in main urls.py"""
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Add in the context dict so the ReportParamSerializer can know how to get the User on the request."""
        # pass in the request to be serialized
        params_serializer = ReportParamsSerializer(
            data=request.GET, context={"request": request})

        params_serializer.is_valid(raise_exception=True)

        # Save serialized params to be used in next step.
        params = params_serializer.save()

        # Pass in the serialized parameters from the request(start_date, end_date and the user). It uses the params to get the right transaction details for the report.
        data = transaction_report(params)

        # Takes the retuen transaction details and serializes it to be returned in the predifned report format.
        serializer = ReportEntrySerializer(instance=data, many=True)
        return Response(data=serializer.data)
