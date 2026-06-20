from django.contrib import admin
from .models import BankTestResult


@admin.register(BankTestResult)
class BankTestResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recommended_bank', 'created_at')
    list_filter = ('recommended_bank', 'created_at')
    search_fields = ('user__username', 'recommended_bank__name')