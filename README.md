# E-commerce Dashboard API

## 1. Project Overview

The E-commerce Dashboard API is a comprehensive backend solution for managing an e-commerce platform. It provides a robust set of endpoints for handling products, categories, customers, orders, and dashboard statistics. The API is designed with a focus on serializer relationships and nested serializers in Django REST Framework, allowing for complex data structures and operations.

This API enables administrators to:
- Manage products and their categories
- Track inventory and product details
- Process customer orders
- View sales statistics and reports
- Monitor customer activity

The project demonstrates advanced Django REST Framework features including relationship fields, nested serializers, custom relationship fields, and handling nested creates and updates.

## 2. Technologies Used

- **Python 3.8+**: Core programming language
- **Django 4.2+**: Web framework
- **Django REST Framework 3.14+**: API toolkit for building RESTful APIs
- **Pillow**: Python Imaging Library for image processing
- **SQLite** (development) / **PostgreSQL** (production): Database systems
- **Django Filter**: For advanced filtering capabilities
- **Django CORS Headers**: For handling Cross-Origin Resource Sharing

## 3. Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (optional but recommended)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-dashboard-api.git
   cd ecommerce-dashboard-api