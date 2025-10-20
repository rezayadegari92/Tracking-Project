# Docker Setup for Shipment Tracking API

This guide explains how to run the Shipment Tracking API using Docker with PostgreSQL 17.

## Prerequisites

- Docker Desktop installed
- Docker Compose installed

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd Tracking-Project
   ```

2. **Build and start services:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Swagger Documentation: http://localhost:8000/api/docs/
   - ReDoc Documentation: http://localhost:8000/api/redoc/
   - Django Admin: http://localhost:8000/admin/

## Available Commands

Use these Docker Compose commands for easy management:

```bash
# Build and start all services
docker-compose up --build

# Start services in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs (recommended for development)
docker-compose logs -f

# Open shell in web container
docker-compose exec web bash

# Run database migrations
docker-compose exec web python manage.py migrate

# Load location data (countries and cities)
docker-compose exec web python manage.py cities_light

# Create Django superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test

# Clean up everything
docker-compose down -v
```

## Manual Docker Commands

If you prefer to use Docker commands directly:

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Run migrations
docker-compose exec web python manage.py migrate

# Load location data (countries and cities)
docker-compose exec web python manage.py cities_light

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run tests
docker-compose exec web python manage.py test
```

## Development Mode

The setup is optimized for development with hot reloading:

```bash
# Start services with live code reloading
docker-compose up

# View logs to see Django output
docker-compose logs -f
```

## Location Data Setup

The application includes worldwide location data for shipment forms. After running migrations, you need to load the location data:

### First-time Setup
```bash
# Load countries and cities data (downloads ~100MB from GeoNames)
docker-compose exec web python manage.py cities_light
```

**Note**: This command downloads location data from GeoNames and may take 5-10 minutes on first run.

### Manual Location Data Loading
```bash
# Using docker-compose
docker-compose exec web python manage.py cities_light
```

### Location Data Details
- **Countries**: All world countries with ISO codes
- **Cities**: Major populated places worldwide
- **Data Source**: GeoNames (geonames.org)
- **Languages**: English only (configured for smaller database)
- **Update**: Run `python manage.py cities_light` to update data

### API Endpoints
Once loaded, location data is available via:
- **Countries**: `GET /api/v1/countries/` (with search)
- **Cities**: `GET /api/v1/cities/` (with country filter and search)

## Database Access

The PostgreSQL database is accessible at:
- Host: localhost
- Port: 5432
- Database: shipment_tracking
- Username: postgres
- Password: postgres

## Environment Variables

The application uses the following environment variables (configured in `.env`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `CORS_ALLOWED_ORIGINS`: Allowed CORS origins

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Change 8001 to any available port
```

### Database Connection Issues
Make sure the database service is healthy:
```bash
docker-compose ps
```

### Permission Issues
On Linux/Mac, you might need to fix permissions:
```bash
sudo chown -R $USER:$USER .
```

### Clean Start
If you encounter issues, try a clean start:
```bash
docker-compose down -v
docker-compose up --build
```

## Production Deployment

For production deployment:

1. Update `.env` with production values
2. Set `DEBUG=False`
3. Use a production database
4. Configure proper CORS origins
5. Set up SSL/TLS
6. Use a reverse proxy (nginx is included)

## API Documentation

Once the services are running, you can access:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Default Admin User

The entrypoint script creates a default admin user:
- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

**Important**: Change these credentials in production!
