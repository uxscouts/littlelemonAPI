from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # 'slug' and 'title' are the fields exposed to the API
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    # This displays the full category details nested inside the menu item JSON
    category = CategorySerializer(read_only=True)
    
    # This field allows you to assign a category using its ID when creating or updating items
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

    def create(self, validated_data):
        # Extract the category_id and fetch the category instance safely
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return MenuItem.objects.create(category=category, **validated_data)
