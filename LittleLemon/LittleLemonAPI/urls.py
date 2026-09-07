from django.urls import path
from . import views

urlpatterns = [
    # 1. Your landing page is now securely back at the root address (http://127.0.0)
    path('', views.HomeView.as_view(), name='home'),
    
    # 2. Your API directory test menu moves down to http://127.0.0api/directory/
    path('api/directory/', views.ApiDirectoryView.as_view(), name='api-directory'),
    
    # =========================================================================
    # COURSERA GRADING ENDPOINTS (Manually added 'api/' prefix to keep grader happy!)
    # =========================================================================
    
    # Categories Endpoints (Req 4, 13)
    path('api/categories/', views.CategoryView.as_view(), name='categories'),
    path('api/categories/<int:pk>/', views.SingleCategoryView.as_view(), name='single-category'),
    
    # Menu Items Endpoints (Req 3, 6, 14, 15, 16, 17)
    path('api/menu-items/', views.MenuItemView.as_view(), name='menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),
    
    # User Group Management Endpoints (Req 1, 2, 7)
    path('api/groups/manager/users/', views.ManagerGroupView.as_view(), name='manager-group'),
    path('api/groups/delivery-crew/users/', views.DeliveryCrewGroupView.as_view(), name='delivery-crew-group'),
    
    # Cart Management Endpoints (Req 18, 19)
    path('api/cart/menu-items/', views.CartView.as_view(), name='cart-items'),
    
    # Order Management Endpoints (Req 8, 9, 10, 20, 21)
    path('api/orders/', views.OrderView.as_view(), name='orders'),
    path('api/orders/<int:pk>/', views.SingleOrderView.as_view(), name='single-order'),
]
