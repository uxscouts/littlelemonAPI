import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LittleLemon.settings')
django.setup()

from LittleLemonAPI.models import Category, MenuItem

def populate_database():
    print("Clearing old data...")
    MenuItem.objects.all().delete()
    Category.objects.all().delete()

    print("Creating categories...")
    # Define our 4 baseline categories
    categories_data = [
        {"title": "Appetizers", "slug": "appetizers"},
        {"title": "Main Courses", "slug": "main-courses"},
        {"title": "Desserts", "slug": "desserts"},
        {"title": "Drinks", "slug": "drinks"},
    ]
    
    categories = {}
    for cat in categories_data:
        category_obj = Category.objects.create(title=cat["title"], slug=cat["slug"])
        categories[cat["title"]] = category_obj

    print("Creating 20 menu items...")
    # List of 20 items to inject
    menu_items = [
        # Appetizers
        {"title": "Greek Salad", "price": 9.99, "featured": True, "category": "Appetizers"},
        {"title": "Bruschetta", "price": 7.50, "featured": False, "category": "Appetizers"},
        {"title": "Calamari", "price": 12.00, "featured": False, "category": "Appetizers"},
        {"title": "Garlic Bread", "price": 5.00, "featured": False, "category": "Appetizers"},
        {"title": "Stuffed Mushrooms", "price": 8.50, "featured": True, "category": "Appetizers"},
        
        # Main Courses
        {"title": "Lemon Herb Chicken", "price": 18.99, "featured": True, "category": "Main Courses"},
        {"title": "Grilled Salmon", "price": 22.50, "featured": False, "category": "Main Courses"},
        {"title": "Ribeye Steak", "price": 28.00, "featured": True, "category": "Main Courses"},
        {"title": "Pasta Carbonara", "price": 15.99, "featured": False, "category": "Main Courses"},
        {"title": "Vegetarian Lasagna", "price": 14.50, "featured": False, "category": "Main Courses"},
        {"title": "Seafood Risotto", "price": 24.00, "featured": False, "category": "Main Courses"},
        
        # Desserts
        {"title": "Tiramisu", "price": 8.50, "featured": True, "category": "Desserts"},
        {"title": "Baklava", "price": 6.99, "featured": False, "category": "Desserts"},
        {"title": "Chocolate Lava Cake", "price": 9.00, "featured": True, "category": "Desserts"},
        {"title": "New York Cheesecake", "price": 7.50, "featured": False, "category": "Desserts"},
        {"title": "Lemon Sorbet", "price": 5.50, "featured": False, "category": "Desserts"},
        
        # Drinks
        {"title": "Lemon Mint Juice", "price": 4.50, "featured": True, "category": "Drinks"},
        {"title": "Iced Latte", "price": 4.00, "featured": False, "category": "Drinks"},
        {"title": "Sparkling Water", "price": 3.00, "featured": False, "category": "Drinks"},
        {"title": "Red Wine Glass", "price": 9.50, "featured": False, "category": "Drinks"},
    ]

    for item in menu_items:
        MenuItem.objects.create(
            title=item["title"],
            price=item["price"],
            featured=item["featured"],
            category=categories[item["category"]] # Link to the Category object
        )

    print("Success! 4 categories and 20 menu items successfully added.")

if __name__ == "__main__":
    populate_database()
