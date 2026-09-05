from django.http import JsonResponse
from .models import Category, MenuItem 


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