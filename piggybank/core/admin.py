from django.contrib import admin

# Register your models here.

from .models import Currency, Transaction, Category

admin.site.register(Currency)
