from dataclasses import dataclass
import datetime
from decimal import Decimal

from django.db.models import Sum, Count, Avg
from django.contrib.auth.models import User

from core.models import Transaction, Category


@dataclass
class ReportEntry:
    """
    This is a dataclass that stores data.
    Serialzer to be created for this in serializers.py.
    """
    category: Category
    total: Decimal
    count: int
    avg: Decimal


@dataclass
class ReportParams:
    """Stores the report parameters."""
    start_date: datetime.datetime
    end_date: datetime.datetime
    user: User


def transaction_report(params: ReportParams):
    """
    '.values()':  to group query result by category.
    '.annotate()': performs an aggregation function on the specified field and creates a new field containing the result of the aggregation.
    """
    data = []
    queryset = Transaction.objects.filter(
        user=params.user,
        date__gte=params.start_date,
        date__lte=params.end_date
    ).values("category").annotate(
        total=Sum("amount"),
        count=Count("id"),
        avg=Avg("amount")
    )

    categories_index = {}
    for category in Category.objects.filter(user=params.user):
        # fetch from database and populate the category_index dict to be used in the upcoming loop. This optimizes the database query since it eliminates querying the database per each item in the loop.
        categories_index[category.pk] = category

    for entry in queryset:
        category = categories_index.get(entry["category"])
        report_entry = ReportEntry(
            category, entry["total"], entry["count"], entry["avg"])
        data.append(report_entry)
    return data
