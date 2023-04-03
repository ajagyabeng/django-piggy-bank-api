from rest_framework import serializers
from django.contrib.auth.models import User

from .reports import ReportParams
from .models import Currency, Category, Transaction


class ReadUserSerializer(serializers.ModelSerializer):
    """Serializes the User object and returns the items in the fields as a read-only. No modifications can be done."""
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")
        read_only_fields = fields


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")


class CategorySerializer(serializers.ModelSerializer):
    """Serializes the Category object. Sets the user field to the currently authenticated user."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = ("id", "name", "user")


class ReadTransactionSerializer(serializers.ModelSerializer):
    user = ReadUserSerializer()
    currency = CurrencySerializer()
    category = CategorySerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "category",
            "user"
        )
        read_only_fields = fields


class WriteTransactionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    """when this serializer is used to create a new object, the user field will be set to the current authenticated user automatically, without the client needing to provide the user information in the request."""
    currency = serializers.SlugRelatedField(
        slug_field="code", queryset=Currency.objects.all())
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = (
            "user",
            "amount",
            "currency",
            "date",
            "description",
            "category"
        )

    def __init__(self, *args, **kwargs):
        """Customize the behavior of a serializer to restrict the available categories based on the authenticated user."""
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["category"].queryset = user.categories.all()


class ReportEntrySerializer(serializers.Serializer):
    """A serializer class to serialize the report view. Create a view in views.py"""
    category = CategorySerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamsSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        """Because the params and ReportParamsSerializer attributes have the same name it can be passed into the ReportParams like below.
        If otherwise, match up the individual attributes.
        """
        return ReportParams(**validated_data)
