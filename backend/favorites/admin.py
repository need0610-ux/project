from django.contrib import admin
from .models import FavoriteProduct


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')