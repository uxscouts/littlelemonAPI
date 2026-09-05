from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Imported for a safe date default

class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True, default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    # FIXED: Added default=0.00 so Django can safely migrate existing database rows
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'menuitem'], name='unique_user_cart_item')
        ]


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_orders", null=True)
    status = models.BooleanField(db_index=True, default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) # Added default just in case
    
    # FIXED: Changed auto_now_add to default=timezone.now. 
    # This provides a default value for migrations AND makes it easier to change or mock dates later!
    date = models.DateField(db_index=True, default=timezone.now) 


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items") 
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'menuitem'], name='unique_order_item')
        ]
