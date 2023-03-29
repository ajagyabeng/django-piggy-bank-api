from rest_framework import serializers

from .models import Currency, Category, Transaction


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "code", "name")
        # fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = ("id", "name")
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        slug_field="code", queryset=Currency.objects.all())

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "date",
            "description",
            "category"
        )


class WriteTransactionSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        slug_field="code", queryset=Currency.objects.all())
    category = serializers.SlugRelatedField(
        slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "currency",
            "date",
            "description",
            "category"
        )


class ReadTransactionSerializer(serializers.ModelSerializer):
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
            "category"
        )
        read_only_fields = fields
