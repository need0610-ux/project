from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/favorites/', include('favorites.urls')),
    path('api/recommendations/', include('recommendations.urls')),
    path('api/community/', include('community.urls')),
    path('api/exchanges/', include('exchanges.urls')),
    path('api/chatbot/', include('chatbot.urls')),
    path('api/maps/', include('maps.urls')),
]