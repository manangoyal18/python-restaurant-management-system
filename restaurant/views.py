from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import datetime

from .models import (
    MenuService, FoodService, TableService, 
    OrderService, OrderItemService, InvoiceService
)


# Menu Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_menus(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        total_count = MenuService.count_menus()
        
        # Pagination
        start_index = (page - 1) * per_page
        menus = MenuService.get_menus(skip=start_index, limit=per_page)
        
        # Convert ObjectId and datetime to string for JSON serialization
        for menu in menus:
            if '_id' in menu:
                menu['_id'] = str(menu['_id'])
            if 'created_at' in menu:
                menu['created_at'] = menu['created_at'].isoformat()
            if 'updated_at' in menu:
                menu['updated_at'] = menu['updated_at'].isoformat()
            if 'start_date' in menu:
                menu['start_date'] = menu['start_date'].isoformat() if hasattr(menu['start_date'], 'isoformat') else str(menu['start_date'])
            if 'end_date' in menu:
                menu['end_date'] = menu['end_date'].isoformat() if hasattr(menu['end_date'], 'isoformat') else str(menu['end_date'])
        
        return Response({
            'success': True,
            'total_count': total_count,
            'menus': menus,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching menus',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_menu(request, menu_id):
    try:
        menu = get_object_or_404(Menu, menu_id=menu_id)
        menu_data = MenuSerializer(menu).data
        
        return Response({
            'success': True,
            'menu': menu_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching menu',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_menu(request):
    try:
        serializer = MenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        menu = serializer.save()
        
        menu_data = MenuSerializer(menu).data
        
        return Response({
            'success': True,
            'message': 'Menu created successfully',
            'menu': menu_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Menu creation failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_menu(request, menu_id):
    try:
        menu = get_object_or_404(Menu, menu_id=menu_id)
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_menu = serializer.save()
        
        menu_data = MenuSerializer(updated_menu).data
        
        return Response({
            'success': True,
            'message': 'Menu updated successfully',
            'menu': menu_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Menu update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Food Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_foods(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        foods = Food.objects.all().order_by('-created_at')
        total_count = foods.count()
        
        # Pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_foods = foods[start_index:end_index]
        
        foods_data = FoodSerializer(paginated_foods, many=True).data
        
        return Response({
            'success': True,
            'total_count': total_count,
            'food_items': foods_data,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while listing food items',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_food(request, food_id):
    try:
        food = get_object_or_404(Food, food_id=food_id)
        food_data = FoodSerializer(food).data
        
        return Response({
            'success': True,
            'food': food_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching the food item',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_food(request):
    try:
        serializer = FoodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Round the price to 2 decimal places
        if 'price' in serializer.validated_data:
            serializer.validated_data['price'] = round(
                float(serializer.validated_data['price']), 2
            )
        
        food = serializer.save()
        food_data = FoodSerializer(food).data
        
        return Response({
            'success': True,
            'message': 'Food item created successfully',
            'food': food_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Food item was not created',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_food(request, food_id):
    try:
        food = get_object_or_404(Food, food_id=food_id)
        serializer = FoodSerializer(food, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Round the price to 2 decimal places if provided
        if 'price' in serializer.validated_data:
            serializer.validated_data['price'] = round(
                float(serializer.validated_data['price']), 2
            )
        
        updated_food = serializer.save()
        food_data = FoodSerializer(updated_food).data
        
        return Response({
            'success': True,
            'message': 'Food item updated successfully',
            'food': food_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Food item update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Table Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_tables(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        tables = Table.objects.all().order_by('table_number')
        total_count = tables.count()
        
        # Pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_tables = tables[start_index:end_index]
        
        tables_data = TableSerializer(paginated_tables, many=True).data
        
        return Response({
            'success': True,
            'total_count': total_count,
            'tables': tables_data,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching tables',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_table(request, table_id):
    try:
        table = get_object_or_404(Table, table_id=table_id)
        table_data = TableSerializer(table).data
        
        return Response({
            'success': True,
            'table': table_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching table',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_table(request):
    try:
        serializer = TableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table = serializer.save()
        
        table_data = TableSerializer(table).data
        
        return Response({
            'success': True,
            'message': 'Table created successfully',
            'table': table_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Table creation failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_table(request, table_id):
    try:
        table = get_object_or_404(Table, table_id=table_id)
        serializer = TableSerializer(table, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_table = serializer.save()
        
        table_data = TableSerializer(updated_table).data
        
        return Response({
            'success': True,
            'message': 'Table updated successfully',
            'table': table_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Table update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Order Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_orders(request):
    try:
        orders = Order.objects.all().order_by('-created_at')
        orders_data = OrderSerializer(orders, many=True).data
        
        return Response({
            'success': True,
            'orders': orders_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while listing order items',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_order(request, order_id):
    try:
        order = get_object_or_404(Order, order_id=order_id)
        order_data = OrderSerializer(order).data
        
        return Response({
            'success': True,
            'order': order_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching the orders',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    try:
        # Set order_date to current time if not provided
        if 'order_date' not in request.data:
            request.data['order_date'] = timezone.now()
        
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        order_data = OrderSerializer(order).data
        
        return Response({
            'success': True,
            'message': 'Order created successfully',
            'order': order_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Order item was not created',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order(request, order_id):
    try:
        order = get_object_or_404(Order, order_id=order_id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()
        
        order_data = OrderSerializer(updated_order).data
        
        return Response({
            'success': True,
            'message': 'Order updated successfully',
            'order': order_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Order item update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Order Item Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_order_items(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        order_items = OrderItem.objects.all().order_by('-created_at')
        total_count = order_items.count()
        
        # Pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_items = order_items[start_index:end_index]
        
        items_data = OrderItemSerializer(paginated_items, many=True).data
        
        return Response({
            'success': True,
            'total_count': total_count,
            'order_items': items_data,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching order items',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_order_item(request, order_item_id):
    try:
        order_item = get_object_or_404(OrderItem, order_item_id=order_item_id)
        item_data = OrderItemSerializer(order_item).data
        
        return Response({
            'success': True,
            'order_item': item_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching order item',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order_item(request):
    try:
        serializer = OrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_item = serializer.save()
        
        item_data = OrderItemSerializer(order_item).data
        
        return Response({
            'success': True,
            'message': 'Order item created successfully',
            'order_item': item_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Order item creation failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_order_item(request, order_item_id):
    try:
        order_item = get_object_or_404(OrderItem, order_item_id=order_item_id)
        serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_item = serializer.save()
        
        item_data = OrderItemSerializer(updated_item).data
        
        return Response({
            'success': True,
            'message': 'Order item updated successfully',
            'order_item': item_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Order item update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


# Invoice Views
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_invoices(request):
    try:
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('recordPerPage', 10))
        
        invoices = Invoice.objects.all().order_by('-created_at')
        total_count = invoices.count()
        
        # Pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_invoices = invoices[start_index:end_index]
        
        invoices_data = InvoiceSerializer(paginated_invoices, many=True).data
        
        return Response({
            'success': True,
            'total_count': total_count,
            'invoices': invoices_data,
            'page': page,
            'per_page': per_page
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching invoices',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_invoice(request, invoice_id):
    try:
        invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
        invoice_data = InvoiceSerializer(invoice).data
        
        return Response({
            'success': True,
            'invoice': invoice_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Error occurred while fetching invoice',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_invoice(request):
    try:
        serializer = InvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()
        
        invoice_data = InvoiceSerializer(invoice).data
        
        return Response({
            'success': True,
            'message': 'Invoice created successfully',
            'invoice': invoice_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Invoice creation failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_invoice(request, invoice_id):
    try:
        invoice = get_object_or_404(Invoice, invoice_id=invoice_id)
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_invoice = serializer.save()
        
        invoice_data = InvoiceSerializer(updated_invoice).data
        
        return Response({
            'success': True,
            'message': 'Invoice updated successfully',
            'invoice': invoice_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Invoice update failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
