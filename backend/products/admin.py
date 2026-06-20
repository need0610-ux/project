from django.contrib import admin
from .models import Bank, FinancialProduct, ProductOption


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(FinancialProduct)
class FinancialProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'product_type', 'name', 'dcls_month')
    list_filter = ('product_type', 'bank')
    search_fields = ('name', 'fin_prdt_cd', 'bank__name')


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'save_trm', 'intr_rate', 'intr_rate2')
    list_filter = ('save_trm',)
    search_fields = ('product__name',)