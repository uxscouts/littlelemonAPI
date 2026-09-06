from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.split_layout.urls if hasattr(admin.site, 'split_layout') else admin.site.urls),
    
    # Requirements 5, 11, 12: Djoser handles user registration and token auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    # Connects your App routes and prefixes them all with 'api/'
    path('api/', include('LittleLemonAPI.urls')), 
]
