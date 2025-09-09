# Django Restaurant Management Backend

A comprehensive restaurant management system built with Django REST Framework and MongoDB, providing APIs for managing users, menus, food items, tables, orders, and invoices.

## Features

- **User Authentication & Authorization**: JWT-based authentication with signup, login, logout, and token refresh
- **User Management**: Complete user CRUD operations with profile management
- **Menu Management**: Create and manage restaurant menus with categories and date ranges
- **Food Management**: Add and manage food items with prices and images
- **Table Management**: Manage restaurant tables with guest capacity
- **Order Management**: Handle customer orders with table assignments
- **Order Item Management**: Manage individual items within orders
- **Invoice Management**: Generate and manage invoices with payment tracking
- **MongoDB Integration**: Document-based storage with Djongo ORM
- **Pagination**: Built-in pagination for all list endpoints
- **Input Validation**: Comprehensive data validation and error handling
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Technology Stack

- **Framework**: Django 5.2.6
- **API**: Django REST Framework 3.16.1
- **Database**: MongoDB with Djongo ORM
- **Authentication**: JWT with djangorestframework-simplejwt
- **Configuration**: python-decouple for environment variables
- **CORS**: django-cors-headers for cross-origin requests

## Project Structure

```
django-restaurant-management/
├── restaurant_management/        # Main Django project
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── authentication/              # User authentication app
│   ├── models.py                # Custom User model
│   ├── serializers.py           # User serializers
│   ├── views.py                 # Authentication views
│   └── urls.py                  # Authentication URLs
├── restaurant/                  # Restaurant management app
│   ├── models.py                # Restaurant models
│   ├── serializers.py           # Restaurant serializers  
│   ├── views.py                 # Restaurant views
│   └── urls.py                  # Restaurant URLs
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- MongoDB (local or cloud)
- pip (Python package manager)

### 1. Clone the Repository

```bash
cd django-restaurant-management
```

### 2. Create Virtual Environment

```bash
python -m venv restaurant_env
```

### 3. Activate Virtual Environment

**Windows:**
```bash
restaurant_env\\Scripts\\activate
```

**macOS/Linux:**
```bash
source restaurant_env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ALLOW_ALL_ORIGINS=True

# Database Configuration
DB_NAME=restaurant
DB_HOST=mongodb://localhost:27017

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### 6. Database Setup

Make sure MongoDB is running on your system, then run:

```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication Endpoints (`/api/auth/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/signup/` | User registration | None |
| POST | `/login/` | User login | None |
| POST | `/logout/` | User logout | Required |
| POST | `/token/refresh/` | Refresh JWT token | None |
| GET | `/users/` | Get all users (paginated) | None |
| GET | `/users/<user_id>/` | Get specific user | None |
| GET | `/profile/` | Get current user profile | Required |
| PUT | `/profile/` | Update user profile | Required |
| POST | `/change-password/` | Change password | Required |

### Menu Endpoints (`/api/menus/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all menus (paginated) | None |
| GET | `/<menu_id>/` | Get specific menu | None |
| POST | `/create/` | Create new menu | Required |
| PUT | `/update/<menu_id>/` | Update menu | Required |

### Food Endpoints (`/api/foods/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all foods (paginated) | None |
| GET | `/<food_id>/` | Get specific food | None |
| POST | `/create/` | Create new food item | Required |
| PUT | `/update/<food_id>/` | Update food item | Required |

### Table Endpoints (`/api/tables/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all tables (paginated) | None |
| GET | `/<table_id>/` | Get specific table | None |
| POST | `/create/` | Create new table | Required |
| PUT | `/update/<table_id>/` | Update table | Required |

### Order Endpoints (`/api/orders/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all orders | None |
| GET | `/<order_id>/` | Get specific order | None |
| POST | `/create/` | Create new order | Required |
| PUT | `/update/<order_id>/` | Update order | Required |

### Order Item Endpoints (`/api/orderItems/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all order items (paginated) | None |
| GET | `/<order_item_id>/` | Get specific order item | None |
| POST | `/create/` | Create new order item | Required |
| PUT | `/update/<order_item_id>/` | Update order item | Required |

### Invoice Endpoints (`/api/invoices/`)

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Get all invoices (paginated) | None |
| GET | `/<invoice_id>/` | Get specific invoice | None |
| POST | `/create/` | Create new invoice | Required |
| PUT | `/update/<invoice_id>/` | Update invoice | Required |

## Data Models

### User Model
- `user_id`: Unique identifier
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: Email address (unique)
- `password`: Hashed password
- `phone`: Phone number (optional)
- `avatar`: Profile picture URL (optional)
- `token`: JWT access token
- `refresh_token`: JWT refresh token
- `created_at`, `updated_at`: Timestamps

### Menu Model
- `menu_id`: Unique identifier
- `name`: Menu name
- `category`: Menu category
- `start_date`: Menu start date
- `end_date`: Menu end date
- `created_at`, `updated_at`: Timestamps

### Food Model
- `food_id`: Unique identifier
- `name`: Food item name
- `price`: Item price (decimal)
- `food_image`: Food image URL (optional)
- `menu_id`: Associated menu ID
- `created_at`, `updated_at`: Timestamps

### Table Model
- `table_id`: Unique identifier
- `table_number`: Table number (unique)
- `number_of_guests`: Guest capacity
- `created_at`, `updated_at`: Timestamps

### Order Model
- `order_id`: Unique identifier
- `order_date`: Order date and time
- `table_id`: Associated table ID (optional)
- `created_at`, `updated_at`: Timestamps

### OrderItem Model
- `order_item_id`: Unique identifier
- `quantity`: Item quantity
- `unit_price`: Price per unit
- `food_id`: Associated food ID
- `order_id`: Associated order ID
- `created_at`, `updated_at`: Timestamps

### Invoice Model
- `invoice_id`: Unique identifier
- `order_id`: Associated order ID
- `payment_method`: Payment method (CARD, CASH, UPI, NET_BANKING)
- `payment_status`: Payment status (PENDING, PAID, FAILED, REFUNDED)
- `payment_due_date`: Due date for payment
- `created_at`, `updated_at`: Timestamps

## Request/Response Examples

### User Registration

**POST** `/api/auth/signup/`

```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "phone": "+1234567890"
}
```

Response:
```json
{
    "success": true,
    "message": "User registered successfully",
    "user": {
        "user_id": "...",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### Create Food Item

**POST** `/api/foods/create/`

```json
{
    "name": "Margherita Pizza",
    "price": 12.99,
    "food_image": "https://example.com/pizza.jpg",
    "menu_id": "menu_123"
}
```

Response:
```json
{
    "success": true,
    "message": "Food item created successfully",
    "food": {
        "food_id": "food_456",
        "name": "Margherita Pizza",
        "price": "12.99",
        "food_image": "https://example.com/pizza.jpg",
        "menu_id": "menu_123",
        "created_at": "2024-01-01T00:00:00Z"
    }
}
```

## Authentication

This API uses JWT (JSON Web Token) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your-access-token>
```

Or use the custom token header:

```
token: <your-access-token>
```

## Error Handling

All API endpoints return consistent error responses:

```json
{
    "success": false,
    "message": "Error description",
    "error": "Detailed error information"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `404`: Not Found
- `500`: Internal Server Error

## Development

### Running Tests

```bash
python manage.py test
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Apps

```bash
python manage.py startapp app_name
```

## Comparison with Go Version

This Django implementation provides the same functionality as the original Go/Gin version with the following improvements:

1. **Better ORM**: Django's ORM with Djongo provides better MongoDB integration
2. **Built-in Admin**: Django admin interface for easy data management
3. **Comprehensive Validation**: Django's built-in validation system
4. **Better Testing**: Django's testing framework for unit and integration tests
5. **Middleware System**: More flexible middleware for authentication and CORS
6. **Serialization**: Django REST Framework serializers for better API responses
7. **Documentation**: Auto-generated API documentation with DRF

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.