from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.split_layout.urls if hasattr(admin.site, 'split_layout') else admin.site.urls), 
    
    # Requirements 5, 11, 12: Djoser handles user registration and token auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
    # CHANGE THIS LINE: Mount the app URLs at the root path
    path('', include('LittleLemonAPI.urls')), 
]
