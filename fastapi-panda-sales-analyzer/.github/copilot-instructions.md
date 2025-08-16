# FastAPI Data Analysis Project Instructions

This is a full-stack Python project with FastAPI backend and Jinja2 frontend for data analysis and management.

## Project Structure
- `main.py` - FastAPI application with REST endpoints and frontend routes
- `templates/` - Jinja2 HTML templates for the frontend
- `static/` - CSS and static assets
- `data/` - CSV data storage
- `requirements.txt` - Python dependencies

## Key Features
- **Backend API Endpoints**:
  - GET `/api/analyze` - Dataset analysis and summary
  - GET `/api/data` - Retrieve top/bottom rows with query parameters
  - POST `/api/data` - Add new records
  - PUT `/api/data/{id}` - Update existing records
  - DELETE `/api/data/{id}` - Delete records

- **Frontend Pages**:
  - `/` - Main dashboard with data visualization
  - `/add` - Add new record form
  - `/edit/{id}` - Edit existing record form
  - `/data_cleaning` - Data cleaning tools and filters

## Development Guidelines
- Use pandas for data manipulation
- Follow FastAPI best practices for API development
- Use Tailwind CSS for consistent UI styling
- Implement proper error handling and validation
- Use Jinja2 templates for server-side rendering
- Keep data persistence simple with CSV files for this demo

## Code Style
- Use async/await for API endpoints
- Include proper type hints
- Add descriptive docstrings for functions
- Use meaningful variable names
- Follow PEP 8 style guidelines
