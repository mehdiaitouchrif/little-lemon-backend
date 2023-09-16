from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Category, MenuItem, Cart, Order, OrderItem, Reservation, MenuItemImage
from django.contrib.auth.models import Group, User
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, UserSerializer, ReservationSerializer, MenuItemImageSerializer
from .permissions import IsManagerOrAdmin
import datetime
    
# Categories
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]


# Menu Items
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.prefetch_related('images').all()
    serializer_class = MenuItemSerializer
    search_fields = ['category__title', 'title']
    ordering_fields = ['price', 'title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsManagerOrAdmin, IsAuthenticated]
        return [permission() for permission in permission_classes]


class MenuItemImageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemImageSerializer
    lookup_url_kwarg = 'pk'  # Use 'pk' as the lookup keyword argument

    def get_queryset(self):
        menu_item_pk = self.kwargs['menu_item_pk']
        return MenuItemImage.objects.filter(menu_item__pk=menu_item_pk)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class MenuItemImageViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemImageSerializer

    def get_serializer_context(self):
        return {'menu_item_id': self.kwargs['menu_item_pk']}

    def get_queryset(self):
        menu_item_pk = self.kwargs['menu_item_pk']
        return MenuItemImage.objects.filter(menu_item__pk=menu_item_pk)

# Cart View
class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("ok")

# Orders
class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: #normal customer
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery crew').exists(): #delivery crew
            return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
        else: #manager
            return Order.objects.all()

    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total


class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count()==0: # Customer
            return Response('Unauthorized to update orders', status=status.HTTP_403_FORBIDDEN)
        else: #everyone else - Super Admin, Manager and Delivery Crew
            return super().update(request, *args, **kwargs)


# Groups
class ManagerViewSet(viewsets.ViewSet):
    permission_classes = [IsManagerOrAdmin]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery crew')
        items = UserSerializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"Unauthorized to assign groups"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Manager').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def is_table_available(self, date, time, num_guests):
        # Check if time is within booking hours (10 AM to 10 PM)
        requested_time = datetime.time.fromisoformat(str(time))
        if not (10 <= requested_time.hour < 22):
            return False

        # Check if table is available for the given date, time, and number of guests
        reservations = Reservation.objects.filter(date=date, time=time)
        total_guests = sum(r.num_guests for r in reservations)
        available_tables = 4 - len(reservations)
        return total_guests + num_guests <= available_tables * 6

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = self.request.user.id
        request.data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Check if table is available at the given date, time, and number of guests
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        num_guests = serializer.validated_data['num_guests']
        if not self.is_table_available(date, time, num_guests):
            return Response({'message': 'Sorry, no tables available for the selected date and time.'})

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReservationUpdateView(APIView):
    def get(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        data = request.data.copy()
        data['user'] = self.request.user.id
        serializer = ReservationSerializer(reservation, data=data)
        if serializer.is_valid():
            if not ReservationListCreateView().is_table_available(serializer.validated_data['date'], serializer.validated_data['time'], serializer.validated_data['num_guests']):
                return Response({'message': 'Table is not available at this time.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return Response({'message': 'Reservation canceled'} ,status=status.HTTP_204_NO_CONTENT)
    