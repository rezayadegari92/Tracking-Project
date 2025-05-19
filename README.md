# Shipment Tracking System

A Django-based shipment tracking system that manages shipping operations, tracking, and delivery management.

## Features

- Shipment management with AWB and reference number generation
- Shipper and receiver information management
- Support for different product types (Document and Non-Document)
- Multiple service types (Inbound, Outbound, Pick-Up Visa)
- Weight and volumetric calculations
- Image upload support for shipments
- Location tracking with city and country support
- COD and payment tracking

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Tracking-Project
```

2. Create and activate virtual environment:
```bash
python -m venv menv
source menv/bin/activate  # On Linux/Mac
# or
menv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `shipments/`: Main app for shipment management
  - `models.py`: Contains Shipment, Shipper, and ShipmentImage models
  - `views.py`: View logic for shipment operations
  - `urls.py`: URL routing for shipment endpoints

## Models

### Shipment
- AWB number (auto-generated)
- Reference number (auto-generated)
- Shipper and receiver details
- Product type (Document/Non-Document)
- Service type (Inbound/Outbound/Pick-Up Visa)
- Weight and volumetric calculations
- Payment information

### Shipper
- Company details
- Contact information
- Location data

### ShipmentImage
- Image upload support for shipments
- Timestamp tracking

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details