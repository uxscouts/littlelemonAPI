from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    # Added db_index=True to slug since it's frequently searched in URLs
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True, default=False) # Added a default
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2) # Added for parity with OrderItem

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'menuitem'], name='unique_user_cart_item')
        ]


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_orders", null=True)
    status = models.BooleanField(db_index=True, default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    # Changed to auto_now_add so it automatically sets the current date when created
    date = models.DateField(db_index=True, auto_now_add=True) 


class OrderItem(models.Model):
    # FIXED: Now points to Order, not User
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items") 
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'menuitem'], name='unique_order_item')
        ]
