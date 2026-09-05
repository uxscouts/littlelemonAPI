from django.http import JsonResponse
from .models import Category, MenuItem 
from django.views.generic import TemplateView
from rest_framework import generics
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


def category_list(request):
  categories = Category.objects.all().values("id", "title", "slug")
  return JsonResponse(list(categories), safe=False)


# 1. Look up by ID
def category_detail_by_id(request, id):
  try:
    category = Category.objects.get(id=id)
    return JsonResponse(
        {"id": category.id, "title": category.title, "slug": category.slug}
    )
  except Category.DoesNotExist:
    return JsonResponse({"error": "Not Found", "message": f"ID {id} does not exist."}, status=404)


# 2. Look up by Slug
def category_detail_by_slug(request, slug):
  try:
    category = Category.objects.get(slug=slug)
    return JsonResponse(
        {"id": category.id, "title": category.title, "slug": category.slug}
    )
  except Category.DoesNotExist:
    return JsonResponse(
        {"error": "Not Found", "message": f"Slug '{slug}' does not exist."},
        status=404,
    )


def menu_item_list(request):
    # Fetch all menu items and select the fields to return
    # 'category__title' uses a double underscore to pull the name of the category
    items = MenuItem.objects.all().values('id', 'title', 'price', 'featured', 'category__title')
    
    data = list(items)
    return JsonResponse(data, safe=False)



class ApiDirectoryView(TemplateView):
    template_name = 'api_directory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Define your endpoints dynamically to loop through them in HTML
        context['endpoints'] = [
            {
                'name': 'Categories',
                'url': '/api/categories/',
                'method': 'GET, POST',
                'description': 'List all food categories or create a new one.'
            },
            {
                'name': 'Menu Items',
                'url': '/api/menu-items/',
                'method': 'GET, POST',
                'description': 'Browse the restaurant menu or add new food items.'
            },
            {
                'name': 'Shopping Cart',
                'url': '/api/cart/',
                'method': 'GET, POST, DELETE',
                'description': 'Manage temporary items inside the current user\'s cart.'
            },
            {
                'name': 'Orders',
                'url': '/api/orders/',
                'method': 'GET, POST',
                'description': 'View order history or checkout active cart items.'
            },
        ]
        return context


    # View for /api/categories/
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# View for /api/menu-items/
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
