from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView
from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from .permissions import IsManager

class HomeView(TemplateView):
    template_name = 'LittleLemonAPI/home.html' # Updated path

# In LittleLemonAPI/views.py
class ApiDirectoryView(TemplateView):
    # Update this line to use the namespaced path!
    template_name = 'LittleLemonAPI/api_directory.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['endpoints'] = [
            {'name': 'Categories', 'url': '/api/categories/', 'method': 'GET, POST', 'description': 'List all food categories or create a new one.'},
            {'name': 'Menu Items', 'url': '/api/menu-items/', 'method': 'GET, POST', 'description': 'Browse the restaurant menu or add new food items.'},
            {'name': 'Shopping Cart', 'url': '/api/cart/menu-items/', 'method': 'GET, POST, DELETE', 'description': 'Manage temporary items inside the current user\'s cart.'},
            {'name': 'Orders', 'url': '/api/orders/', 'method': 'GET, POST', 'description': 'View order history or checkout active cart items.'},
        ]
        return context



# --- CATEGORIES ENDPOINTS ---
# Handles GET /api/categories and POST /api/categories
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Requirements 4: Admin can add categories. Customers can browse.
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.AllowAny()]

# Handles GET /api/categories/<int:pk> and DELETE /api/categories/<int:pk>
class SingleCategoryView(generics.RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [permissions.AllowAny()]


# --- MENU ITEMS ENDPOINTS ---
# Handles GET /api/menu-items and POST /api/menu-items
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    # Requirements 15, 16, 17: Filtering, Sorting by price, and Pagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']  # Allows browsing by category
    ordering_fields = ['price']      # Allows sorting by price
    search_fields = ['title']

    def get_permissions(self):
        # Requirement 3: Admin can add menu items. Customers can browse.
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [permissions.AllowAny()]

# Handles GET, PUT, PATCH, DELETE for /api/menu-items/<int:pk>
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsManager()] # Requirement 6: Managers can update item of the day
        return [permissions.AllowAny()]




from .models import Cart, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer
from django.db import transaction


# --- GROUP MANAGEMENT ---
# Handles Admin listing and updating Managers
class ManagerGroupView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        managers = User.objects.filter(groups__name='Manager')
        # Simple structural representation for user lists
        data = [{"id": u.id, "username": u.username, "email": u.email} for u in managers]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": f"User '{username}' added to Manager group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message": f"User '{username}' removed from Manager group"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Handles Managers listing and updating Delivery Crew
class DeliveryCrewGroupView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        crew = User.objects.filter(groups__name='Delivery Crew')
        data = [{"id": u.id, "username": u.username, "email": u.email} for u in crew]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            crew = Group.objects.get(name="Delivery Crew")
            crew.user_set.add(user)
            return Response({"message": f"User '{username}' added to Delivery Crew group"}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        username = request.data.get('username')
        if not username:
            return Response({"error": "Username required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
            crew = Group.objects.get(name="Delivery Crew")
            crew.user_set.remove(user)
            return Response({"message": f"User '{username}' removed from Delivery Crew group"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)



# --- CART MANAGEMENT ---
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # We pass request context to the serializer to automatically identify the auth user
        serializer = CartSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Flushes all items in the current customer's cart
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart flushed successfully"}, status=status.HTTP_204_NO_CONTENT)



# --- ORDER MANAGEMENT ---
class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.groups.filter(name='Manager').exists() or request.user.is_superuser:
            orders = Order.objects.all()
        elif request.user.groups.filter(name='Delivery Crew').exists():
            orders = Order.objects.filter(delivery_crew=request.user)
        else:
            orders = Order.objects.filter(customer=request.user) # Using your preferred 'customer' field!
            
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Atomically bundle operations so a failure rolls back the DB state cleanly
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Your shopping cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Calculate running total across cart entries
            total_cost = sum(item.price for item in cart_items)
            
            # Create the main Order shell record
            order = Order.objects.create(
                customer=request.user,
                total=total_cost
            )
            
            # Transfer rows from Cart into individual OrderItems entries
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menuitem=item.menuitem,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    price=item.price
                )
            
            # Clean out the checkout buffer
            cart_items.delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SingleOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # --- 1. GET A SPECIFIC ORDER ---
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Enforce Customer Boundaries
        is_manager = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
        is_crew = request.user.groups.filter(name='Delivery Crew').exists()
        
        if not is_manager and not is_crew and order.customer != request.user:
            return Response({"error": "You do not have permission to view this order."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- 2. UPDATE A SPECIFIC ORDER (PATCH) ---
    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        is_manager = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
        is_crew = request.user.groups.filter(name='Delivery Crew').exists()

        # Regular Customers are NOT allowed to patch orders after they are placed!
        if not is_manager and not is_crew:
            return Response({"error": "Customers cannot modify orders after submission."}, status=status.HTTP_403_FORBIDDEN)

        # Delivery Crew can ONLY update the status field!
        if is_crew and not is_manager:
            # If they try to modify anything other than 'status', block it
            if any(key != 'status' for key in request.data.keys()):
                return Response({"error": "Delivery crew can only update order status."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- 3. DELETE AN ORDER ---
    def delete(self, request, pk):
        # Only Managers can permanently delete records
        if not request.user.groups.filter(name='Manager').exists() and not request.user.is_superuser:
            return Response({"error": "Only managers can delete orders."}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

