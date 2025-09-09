from rest_framework import serializers
from .models import Menu, Food, Table, Order, OrderItem, Invoice
from django.utils import timezone
from decimal import Decimal


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ('menu_id', 'created_at', 'updated_at')

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise serializers.ValidationError(
                    "Start date must be before end date."
                )
        
        return attrs


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ('food_id', 'created_at', 'updated_at')

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return round(value, 2)

    def validate_menu_id(self, value):
        try:
            Menu.objects.get(menu_id=value)
        except Menu.DoesNotExist:
            raise serializers.ValidationError("Menu not found.")
        return value


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ('table_id', 'created_at', 'updated_at')

    def validate_number_of_guests(self, value):
        if value < 1 or value > 20:
            raise serializers.ValidationError(
                "Number of guests must be between 1 and 20."
            )
        return value

    def validate_table_number(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Table number must be greater than 0."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_id', 'created_at', 'updated_at')

    def validate_table_id(self, value):
        if value:  # table_id is optional
            try:
                Table.objects.get(table_id=value)
            except Table.DoesNotExist:
                raise serializers.ValidationError("Table not found.")
        return value

    def validate_order_date(self, value):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Order date cannot be in the future."
            )
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('order_item_id', 'created_at', 'updated_at', 'total_price')

    def validate_quantity(self, value):
        if value < 1 or value > 100:
            raise serializers.ValidationError(
                "Quantity must be between 1 and 100."
            )
        return value

    def validate_unit_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Unit price must be greater than 0.")
        return round(value, 2)

    def validate_food_id(self, value):
        try:
            Food.objects.get(food_id=value)
        except Food.DoesNotExist:
            raise serializers.ValidationError("Food item not found.")
        return value

    def validate_order_id(self, value):
        try:
            Order.objects.get(order_id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('invoice_id', 'created_at', 'updated_at')

    def validate_order_id(self, value):
        try:
            Order.objects.get(order_id=value)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")
        return value

    def validate_payment_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "Payment due date cannot be in the past."
            )
        return value


# Detailed serializers for responses with related data
class FoodDetailSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(source='menu_id', read_only=True)

    class Meta:
        model = Food
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    table = TableSerializer(source='table_id', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemDetailSerializer(serializers.ModelSerializer):
    food = FoodDetailSerializer(source='food_id', read_only=True)
    order = OrderSerializer(source='order_id', read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(source='order_id', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'


# Summary serializers for aggregated data
class OrderSummarySerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    orders_by_status = serializers.DictField()


class FoodSummarySerializer(serializers.Serializer):
    total_foods = serializers.IntegerField()
    foods_by_menu = serializers.DictField()
    price_range = serializers.DictField()


class TableSummarySerializer(serializers.Serializer):
    total_tables = serializers.IntegerField()
    total_capacity = serializers.IntegerField()
    occupied_tables = serializers.IntegerField()
    available_tables = serializers.IntegerField()