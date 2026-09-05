from django.urls import path
from .views import category_detail, category_list

urlpatterns = [
    path("categories/", category_list, name="category_list"),
   # path("category/<slug:slug>/", category_detail, name="category_detail"),
    path("categories/<int:id>/", category_detail, name="category_detail"),
]