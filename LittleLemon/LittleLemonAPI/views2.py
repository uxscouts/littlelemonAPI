# no render because you out put as JSON
#from django.shortcuts import get_object_or_404, render

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Category




# view all categories - for HTML template not JSON
#def category_list(request):
  #categories = Category.objects.all()
  #return(request, "category_list.html", {"categories": categories})

  
# 1. GET /api/categories/ - for JSON output
def category_list(request):
  # Fetch all rows and convert them into a list of dictionaries
  categories = Category.objects.all().values("id", "title", "slug")
  data = list(categories)

  # safe=False allows us to pass a list instead of a dictionary
  return JsonResponse(data, safe=False)


# view single category - for HTML template not JSON
#def category_detail(request, slug):
  #category = get_object_or_404(Category, slug=slug)
  #return render(request, "category_detail.html", {"category": category})


  # 2. GET /api/categories/<id>/ - output as JSON not HTML template
from django.http import JsonResponse
from .models import Category


def category_detail(request, id):
  try:
    # Attempt to fetch the category by its ID
    category = Category.objects.get(id=id)

    # Return successful data payload
    data = {
        "id": category.id,
        "title": category.title,
        "slug": category.slug,
    }
    return JsonResponse(data)

  except Category.DoesNotExist:
    # Build a helpful JSON error payload
    error_payload = {
        "error": "Not Found",
        "status_code": 404,
        "message": f"Category with ID {id} does not exist in the LittleLemon database.",
    }
    # status=404 explicitly changes the HTTP response code from 200 to 404
    return JsonResponse(error_payload, status=404)
