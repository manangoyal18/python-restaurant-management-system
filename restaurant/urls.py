from django.urls import path
from . import views

urlpatterns = [
    # Menu endpoints
    path('menus/', views.get_menus, name='get-menus'),
    path('menus/<str:menu_id>/', views.get_menu, name='get-menu'),
    path('menus/create/', views.create_menu, name='create-menu'),
    path('menus/update/<str:menu_id>/', views.update_menu, name='update-menu'),
    
    # Food endpoints
    path('foods/', views.get_foods, name='get-foods'),
    path('foods/<str:food_id>/', views.get_food, name='get-food'),
    path('foods/create/', views.create_food, name='create-food'),
    path('foods/update/<str:food_id>/', views.update_food, name='update-food'),
    
    # Table endpoints
    path('tables/', views.get_tables, name='get-tables'),
    path('tables/<str:table_id>/', views.get_table, name='get-table'),
    path('tables/create/', views.create_table, name='create-table'),
    path('tables/update/<str:table_id>/', views.update_table, name='update-table'),
    
    # Order endpoints
    path('orders/', views.get_orders, name='get-orders'),
    path('orders/<str:order_id>/', views.get_order, name='get-order'),
    path('orders/create/', views.create_order, name='create-order'),
    path('orders/update/<str:order_id>/', views.update_order, name='update-order'),
    
    # Order Item endpoints
    path('orderItems/', views.get_order_items, name='get-order-items'),
    path('orderItems/<str:order_item_id>/', views.get_order_item, name='get-order-item'),
    path('orderItems/create/', views.create_order_item, name='create-order-item'),
    path('orderItems/update/<str:order_item_id>/', views.update_order_item, name='update-order-item'),
    
    # Invoice endpoints
    path('invoices/', views.get_invoices, name='get-invoices'),
    path('invoices/<str:invoice_id>/', views.get_invoice, name='get-invoice'),
    path('invoices/create/', views.create_invoice, name='create-invoice'),
    path('invoices/update/<str:invoice_id>/', views.update_invoice, name='update-invoice'),
]