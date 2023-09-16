from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, MenuItem, Cart, Order, OrderItem, Reservation, Occasion, MenuItemImage


class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        menu_item_id = self.context['menu_item_id']        
        return MenuItemImage.objects.create(menu_item_id=menu_item_id, **validated_data)

    class Meta: 
        model = MenuItemImage
        fields = ['id', 'image']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    images = MenuItemImageSerializer(many=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured', 'images']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class ReservationSerializer(serializers.ModelSerializer):
    occasion = serializers.ChoiceField(choices=Occasion.choices)
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'date', 'time', 'num_guests', 'occasion', 'message']
