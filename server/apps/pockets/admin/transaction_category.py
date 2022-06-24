from django.contrib import admin

from ..models import TransactionCategory


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'user')
    list_filter = ('category_type',)
    search_fields = ('name', 'category_type', 'user')
