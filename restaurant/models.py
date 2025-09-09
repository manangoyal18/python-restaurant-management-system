from datetime import datetime
from restaurant_management.database import (
    MenuModel, FoodModel, TableModel, OrderModel, OrderItemModel, InvoiceModel
)


class MenuService:
    @staticmethod
    def create_menu(data):
        """Create a new menu"""
        menu_data = {
            'name': data['name'],
            'category': data['category'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return MenuModel.create(menu_data)
    
    @staticmethod
    def get_menu(menu_id):
        """Get a menu by ID"""
        return MenuModel.find_one({'menu_id': menu_id})
    
    @staticmethod
    def get_menus(skip=0, limit=None, sort=None):
        """Get all menus with pagination"""
        if sort is None:
            sort = [('created_at', -1)]
        return MenuModel.find_many(skip=skip, limit=limit, sort=sort)
    
    @staticmethod
    def count_menus():
        """Count total menus"""
        return MenuModel.count()
    
    @staticmethod
    def update_menu(menu_id, data):
        """Update a menu"""
        data['updated_at'] = datetime.utcnow()
        return MenuModel.update_one({'menu_id': menu_id}, data)


class FoodService:
    @staticmethod
    def create_food(data):
        """Create a new food item"""
        food_data = {
            'name': data['name'],
            'price': float(data['price']),
            'food_image': data.get('food_image'),
            'menu_id': data['menu_id'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return FoodModel.create(food_data)
    
    @staticmethod
    def get_food(food_id):
        """Get a food item by ID"""
        return FoodModel.find_one({'food_id': food_id})
    
    @staticmethod
    def get_foods(skip=0, limit=None, sort=None):
        """Get all foods with pagination"""
        if sort is None:
            sort = [('created_at', -1)]
        return FoodModel.find_many(skip=skip, limit=limit, sort=sort)
    
    @staticmethod
    def count_foods():
        """Count total foods"""
        return FoodModel.count()
    
    @staticmethod
    def update_food(food_id, data):
        """Update a food item"""
        if 'price' in data:
            data['price'] = float(data['price'])
        data['updated_at'] = datetime.utcnow()
        return FoodModel.update_one({'food_id': food_id}, data)


class TableService:
    @staticmethod
    def create_table(data):
        """Create a new table"""
        table_data = {
            'table_number': data['table_number'],
            'number_of_guests': data['number_of_guests'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return TableModel.create(table_data)
    
    @staticmethod
    def get_table(table_id):
        """Get a table by ID"""
        return TableModel.find_one({'table_id': table_id})
    
    @staticmethod
    def get_tables(skip=0, limit=None, sort=None):
        """Get all tables with pagination"""
        if sort is None:
            sort = [('table_number', 1)]
        return TableModel.find_many(skip=skip, limit=limit, sort=sort)
    
    @staticmethod
    def count_tables():
        """Count total tables"""
        return TableModel.count()
    
    @staticmethod
    def update_table(table_id, data):
        """Update a table"""
        data['updated_at'] = datetime.utcnow()
        return TableModel.update_one({'table_id': table_id}, data)


class OrderService:
    @staticmethod
    def create_order(data):
        """Create a new order"""
        order_data = {
            'order_date': data['order_date'],
            'table_id': data.get('table_id'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return OrderModel.create(order_data)
    
    @staticmethod
    def get_order(order_id):
        """Get an order by ID"""
        return OrderModel.find_one({'order_id': order_id})
    
    @staticmethod
    def get_orders(skip=0, limit=None, sort=None):
        """Get all orders with pagination"""
        if sort is None:
            sort = [('created_at', -1)]
        return OrderModel.find_many(skip=skip, limit=limit, sort=sort)
    
    @staticmethod
    def count_orders():
        """Count total orders"""
        return OrderModel.count()
    
    @staticmethod
    def update_order(order_id, data):
        """Update an order"""
        data['updated_at'] = datetime.utcnow()
        return OrderModel.update_one({'order_id': order_id}, data)


class OrderItemService:
    @staticmethod
    def create_order_item(data):
        """Create a new order item"""
        order_item_data = {
            'quantity': data['quantity'],
            'unit_price': float(data['unit_price']),
            'food_id': data['food_id'],
            'order_id': data['order_id'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return OrderItemModel.create(order_item_data)
    
    @staticmethod
    def get_order_item(order_item_id):
        """Get an order item by ID"""
        item = OrderItemModel.find_one({'order_item_id': order_item_id})
        if item:
            item['total_price'] = item['quantity'] * item['unit_price']
        return item
    
    @staticmethod
    def get_order_items(skip=0, limit=None, sort=None):
        """Get all order items with pagination"""
        if sort is None:
            sort = [('created_at', -1)]
        items = OrderItemModel.find_many(skip=skip, limit=limit, sort=sort)
        # Add total_price to each item
        for item in items:
            item['total_price'] = item['quantity'] * item['unit_price']
        return items
    
    @staticmethod
    def count_order_items():
        """Count total order items"""
        return OrderItemModel.count()
    
    @staticmethod
    def update_order_item(order_item_id, data):
        """Update an order item"""
        if 'unit_price' in data:
            data['unit_price'] = float(data['unit_price'])
        data['updated_at'] = datetime.utcnow()
        return OrderItemModel.update_one({'order_item_id': order_item_id}, data)


class InvoiceService:
    @staticmethod
    def create_invoice(data):
        """Create a new invoice"""
        invoice_data = {
            'order_id': data['order_id'],
            'payment_method': data['payment_method'],
            'payment_status': data['payment_status'],
            'payment_due_date': data['payment_due_date'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        return InvoiceModel.create(invoice_data)
    
    @staticmethod
    def get_invoice(invoice_id):
        """Get an invoice by ID"""
        return InvoiceModel.find_one({'invoice_id': invoice_id})
    
    @staticmethod
    def get_invoices(skip=0, limit=None, sort=None):
        """Get all invoices with pagination"""
        if sort is None:
            sort = [('created_at', -1)]
        return InvoiceModel.find_many(skip=skip, limit=limit, sort=sort)
    
    @staticmethod
    def count_invoices():
        """Count total invoices"""
        return InvoiceModel.count()
    
    @staticmethod
    def update_invoice(invoice_id, data):
        """Update an invoice"""
        data['updated_at'] = datetime.utcnow()
        return InvoiceModel.update_one({'invoice_id': invoice_id}, data)
