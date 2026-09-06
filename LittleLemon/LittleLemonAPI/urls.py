from django.urls import path
from . import views

urlpatterns = [
    # 0. API Directory Template Root
    path('', views.ApiDirectoryView.as_view(), name='api-directory'),

    # 1. Categories Endpoints (Req 4, 13)
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.SingleCategoryView.as_view(), name='single-category'),

    # 2. Menu Items Endpoints (Req 3, 6, 14, 15, 16, 17)
    path('menu-items/', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='single-menu-item'),

    # 3. User Group Management Endpoints (Req 1, 2, 7)
    path('groups/manager/users/', views.ManagerGroupView.as_view(), name='manager-group'),
    path('groups/delivery-crew/users/', views.DeliveryCrewGroupView.as_view(), name='delivery-crew-group'),

    # 4. Cart Management Endpoints (Req 18, 19)
    path('cart/menu-items/', views.CartView.as_view(), name='cart-items'),

    # 5. Order Management Endpoints (Req 8, 9, 10, 20, 21)
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.SingleOrderView.as_view(), name='single-order'),
]
