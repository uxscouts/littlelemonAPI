from django.urls import path
from .views import category_detail_by_id, category_detail_by_slug, category_list, menu_item_list

urlpatterns = [
    path("categories/", category_list, name="category_list"),
    # Route 1: Looks up by database integer ID
    path("categories/<int:id>/", category_detail_by_id, name="category_detail_id"),
    # Route 2: Looks up by text slug string
    path("categories/<slug:slug>/", category_detail_by_slug, name="category_detail_slug"),
    path("menu-items/", menu_item_list, name="menu_item_list"),
]
