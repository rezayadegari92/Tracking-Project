# Shipment Tracking API

A comprehensive Django REST Framework API for shipment tracking and management system.

## Features

- **User Authentication**: JWT-based authentication with registration, login, and profile management
- **Shipment Management**: Create, track, and manage shipments with detailed information
- **PDF Generation**: Generate confirmation, detailed, and label PDFs for shipments
- **Public Tracking**: Track shipments by AWB or REF numbers without authentication
- **Admin Interface**: Django admin interface for managing shipments and users
- **API Documentation**: Comprehensive Swagger/OpenAPI documentation

## API Endpoints

### Authentication
- `POST /api/v1/accounts/register/` - Register new user
- `POST /api/v1/accounts/login/` - Login and get JWT tokens
- `POST /api/v1/accounts/logout/` - Logout and blacklist token
- `GET /api/v1/accounts/profile/` - Get user profile
- `PATCH /api/v1/accounts/profile/` - Update user profile
- `POST /api/v1/accounts/password/change/` - Change password
- `POST /api/v1/accounts/token/refresh/` - Refresh JWT token

### Shipments
- `GET /api/v1/shipments/countries/` - List all countries
- `GET /api/v1/shipments/cities/` - List cities (filtered by country)
- `POST /api/v1/shipments/` - Create new shipment
- `GET /api/v1/shipments/track/` - Track shipment by AWB/REF number
- `GET /api/v1/shipments/list/` - List user's shipments (authenticated)
- `GET /api/v1/shipments/{id}/` - Get shipment details (authenticated)
- `GET /api/v1/shipments/{id}/pdf/confirmation/` - Generate confirmation PDF
- `GET /api/v1/shipments/{id}/pdf/detailed/` - Generate detailed PDF (admin only)
- `GET /api/v1/shipments/{id}/pdf/label/` - Generate label PDF (admin only)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Tracking-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Authentication

This API uses JWT (JSON Web Token) authentication:

1. **Register**: `POST /api/v1/accounts/register/`
2. **Login**: `POST /api/v1/accounts/login/` - Returns access and refresh tokens
3. **Use Token**: Include `Authorization: Bearer <access_token>` in request headers
4. **Refresh Token**: Use refresh token to get new access tokens when they expire

### Example Authentication Flow

```bash
# Register a new user
curl -X POST http://localhost:8000/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Use the returned access token
curl -X GET http://localhost:8000/api/v1/accounts/profile/ \
  -H "Authorization: Bearer <access_token>"
```

## Usage Examples

### Create a Shipment

```bash
curl -X POST http://localhost:8000/api/v1/shipments/ \
  -H "Content-Type: application/json" \
  -d '{
    "shipper": {
      "shipper_name": "John Doe",
      "address": "123 Main St",
      "country_id": 1,
      "city_id": 1,
      "contact_person": "John Doe",
      "contact_number": "1234567890"
    },
    "receiver_name": "Jane Smith",
    "receiver_address": "456 Oak Ave",
    "receiver_country": 1,
    "receiver_city": 1,
    "receiver_contact_person": "Jane Smith",
    "receiver_contact_number": "0987654321",
    "product_type": "doc",
    "service": "outbound",
    "quantity": 1,
    "grossweight": 1.0,
    "width": 10.0,
    "length": 10.0,
    "height": 10.0,
    "item_description": "Important documents"
  }'
```

### Track a Shipment

```bash
curl -X GET "http://localhost:8000/api/v1/shipments/track/?tracking_number=AWB-123456"
```

### Get Countries

```bash
curl -X GET http://localhost:8000/api/v1/shipments/countries/
```

### Get Cities (filtered by country)

```bash
curl -X GET "http://localhost:8000/api/v1/shipments/cities/?country=1"
```

## Project Structure

```
Tracking-Project/
├── accounts/
│   ├── api/v1/          # Accounts API
│   ├── models.py        # User models
│   └── admin.py         # Admin configuration
├── shipments/
│   ├── api/v1/          # Shipments API
│   ├── models.py        # Shipment models
│   ├── utils/           # PDF generation utilities
│   └── templates/pdf/   # PDF templates
├── core/
│   ├── settings.py      # Django settings
│   ├── urls.py         # Main URL configuration
│   └── swagger.py       # API documentation
└── requirements.txt     # Dependencies
```

## Technologies Used

- **Django 4.2**: Web framework
- **Django REST Framework**: API framework
- **JWT Authentication**: Secure token-based authentication
- **WeasyPrint**: PDF generation
- **Swagger/OpenAPI**: API documentation
- **CORS**: Cross-origin resource sharing
- **Django Cities Light**: Country/city data

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

The project follows PEP 8 style guidelines. Use black for code formatting:

```bash
pip install black
black .
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure CORS settings for your frontend domain
5. Set up proper logging
6. Use environment variables for sensitive settings

## License

This project is licensed under the MIT License.