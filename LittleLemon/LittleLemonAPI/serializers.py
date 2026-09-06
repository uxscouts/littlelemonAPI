from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

# --- CATEGORY & MENU ITEM SERIALIZERS ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # Displays category details neatly in JSON responses
    category = CategorySerializer(read_only=True)
    # Allows assigning by ID when creating/updating items
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return MenuItem.objects.create(category=category, **validated_data)


# --- CART SERIALIZERS ---
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem

# --- CATEGORY & MENU ITEM SERIALIZERS ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    # Displays category details neatly in JSON responses
    category = CategorySerializer(read_only=True)
    # Allows assigning by ID when creating/updating items
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return MenuItem.objects.create(category=category, **validated_data)


# --- CART SERIALIZERS ---
class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    
    # Prices are auto-calculated in the save method, so they are read-only to clients
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        
    def validate(self, attrs):
        # Gracefully handle your modern UniqueConstraint verification
        user = self.context['request'].user
        menuitem_id = attrs.get('menuitem_id')
        
        if Cart.objects.filter(user=user, menuitem_id=menuitem_id).exists():
            raise serializers.ValidationError(
                {"detail": "This item is already in your cart. Update the quantity instead."}
            )
        return attrs

    def create(self, validated_data):
        menuitem_id = validated_data.pop('menuitem_id')
        menuitem = MenuItem.objects.get(id=menuitem_id)
        quantity = validated_data.get('quantity')
        
        # Calculate sub-totals dynamically
        unit_price = menuitem.price
        price = unit_price * quantity
        
        return Cart.objects.create(
            menuitem=menuitem, 
            unit_price=unit_price, 
            price=price, 
            **validated_data
        )


# --- ORDER SERIALIZERS ---
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Uses your clean 'customer' label over Coursera's confusing 'user' layout
    customer = serializers.ReadOnlyField(source='customer.username')
    
    # Nesting the detailed lines directly inside the order object
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    
    # Restricts the delivery crew dropdown safely to the specified group users
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Delivery Crew'),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'delivery_crew', 'status', 'total', 'date', 'order_items']
        read_only_fields = ['id', 'customer', 'total', 'date', 'order_items']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Requirement 8: Managers can assign crew and change status
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            instance.delivery_crew = validated_data.get('delivery_crew', instance.delivery_crew)
            instance.status = validated_data.get('status', instance.status)
        
        # Requirement 10: Delivery crew can update status, but CANNOT change assignment fields
        elif user.groups.filter(name='Delivery Crew').exists():
            if 'delivery_crew' in validated_data:
                raise serializers.ValidationError(
                    {"detail": "Delivery crew members are not authorized to reassign orders."}
                )
            instance.status = validated_data.get('status', instance.status)
            
        else:
            raise serializers.ValidationError(
                {"detail": "You do not have permission to modify this transaction record."}
            )

        instance.save()
        return instance

    # Prices are auto-calculated in the save method, so they are read-only to clients
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        
    def validate(self, attrs):
        # Gracefully handle your modern UniqueConstraint verification
        user = self.context['request'].user
        menuitem_id = attrs.get('menuitem_id')
        
        if Cart.objects.filter(user=user, menuitem_id=menuitem_id).exists():
            raise serializers.ValidationError(
                {"detail": "This item is already in your cart. Update the quantity instead."}
            )
        return attrs

    def create(self, validated_data):
        menuitem_id = validated_data.pop('menuitem_id')
        menuitem = MenuItem.objects.get(id=menuitem_id)
        quantity = validated_data.get('quantity')
        
        # Calculate sub-totals dynamically
        unit_price = menuitem.price
        price = unit_price * quantity
        
        return Cart.objects.create(
            menuitem=menuitem, 
            unit_price=unit_price, 
            price=price, 
            **validated_data
        )


# --- ORDER SERIALIZERS ---
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    # Uses your clean 'customer' label over Coursera's confusing 'user' layout
    customer = serializers.ReadOnlyField(source='customer.username')
    
    # Nesting the detailed lines directly inside the order object
    order_items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    
    # Restricts the delivery crew dropdown safely to the specified group users
    delivery_crew = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name='Delivery Crew'),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'delivery_crew', 'status', 'total', 'date', 'order_items']
        read_only_fields = ['id', 'customer', 'total', 'date', 'order_items']

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Requirement 8: Managers can assign crew and change status
        if user.groups.filter(name='Manager').exists() or user.is_superuser:
            instance.delivery_crew = validated_data.get('delivery_crew', instance.delivery_crew)
            instance.status = validated_data.get('status', instance.status)
        
        # Requirement 10: Delivery crew can update status, but CANNOT change assignment fields
        elif user.groups.filter(name='Delivery Crew').exists():
            if 'delivery_crew' in validated_data:
                raise serializers.ValidationError(
                    {"detail": "Delivery crew members are not authorized to reassign orders."}
                )
            instance.status = validated_data.get('status', instance.status)
            
        else:
            raise serializers.ValidationError(
                {"detail": "You do not have permission to modify this transaction record."}
            )

        instance.save()
        return instance
