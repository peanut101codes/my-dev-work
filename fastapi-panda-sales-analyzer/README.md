# FastAPI Sales Data Analysis Dashboard

A full-stack Python web application for sales data analysis and management, built with FastAPI backend and Jinja2 frontend.

## Features

### Backend API
- **GET `/api/analyze`** - Comprehensive dataset analysis including:
  - Dataset information (records, columns, memory usage)
  - Missing value analysis
  - Data type information
  - Numeric and categorical summaries
  
- **GET `/api/data`** - Flexible data retrieval with query parameters:
  - `position`: "top" or "bottom" rows
  - `limit`: Number of rows to return (1-100)
  
- **POST `/api/data`** - Add new order records with form data
- **PUT `/api/data/{order_number}`** - Update existing order records
- **DELETE `/api/data/{order_number}`** - Delete order records

### Frontend Features
- **Dashboard** (`/`) - Interactive sales data visualization with:
  - Statistical summary cards (Total Orders, Sales, Average Order Value)
  - Order data table with edit/delete actions
  - Product line distribution chart
  - Dataset analysis modal
  
- **Add Order** (`/add`) - Form interface for adding new orders
- **Edit Order** (`/edit/{order_number}`) - Form interface for editing existing orders
- **Data Cleaning** (`/data_cleaning`) - Data quality tools including:
  - Missing value detection
  - Duplicate record identification
  - Data type validation
  - Filtering and search capabilities

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Jinja2 templates, Tailwind, Chart.js
- **Data Processing**: Pandas, NumPy
- **Data Storage**: CSV files (easily replaceable with database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd my-fastApi-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
   - **Web Interface**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative API Docs**: http://localhost:8000/redoc

## Project Structure

```
my-fastApi-project/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── data/
│   └── sample_data.csv    # Sample automobile sales dataset
├── templates/
│   ├── index.html         # Main dashboard
│   ├── add_record.html    # Add record form
│   ├── edit_record.html   # Edit record form
│   └── data_cleaning.html # Data cleaning interface
├── static/
│   └── css/
│       └── style.css      # Custom styles
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

## Sample Data

[kaggle.com](https://www.kaggle.com)


## API Usage Examples

### Get Dataset Analysis
```bash
curl http://localhost:8000/api/analyze
```

### Get Top 5 Records
```bash
curl "http://localhost:8000/api/data?position=top&limit=5"
```

### Add New Record
```bash
curl -X POST http://localhost:8000/api/data \
  -F "ORDERNUMBER=10108" \
  -F "QUANTITYORDERED=25" \
  -F "PRICEEACH=120.50" \
  -F "ORDERLINENUMBER=3" \
  -F "SALES=3012.5" \
  -F "ORDERDATE=25/02/2018" \
  -F "DAYS_SINCE_LASTORDER=30" \
  -F "STATUS=Shipped" \
  -F "PRODUCTLINE=Motorcycles" \
  -F "MSRP=120" \
  -F "PRODUCTCODE=S10_1949" \
  -F "CUSTOMERNAME=Toy Universe Inc." \
  -F "PHONE=2125559999" \
  -F "ADDRESSLINE1=123 Main Street" \
  -F "CITY=NYC" \
  -F "POSTALCODE=10023" \
  -F "COUNTRY=USA" \
  -F "CONTACTLASTNAME=Smith" \
  -F "CONTACTFIRSTNAME=Jane" \
  -F "DEALSIZE=Medium"
  -F "POSTALCODE=10023" \
  -F "COUNTRY=USA" \
  -F "CONTACTLASTNAME=Smith" \
  -F "CONTACTFIRSTNAME=Jane" \
  -F "DEALSIZE=Medium"
```

### Update Record
```bash
curl -X PUT http://localhost:8000/api/data/10107 \
  -F "ORDERNUMBER=10107" \
  -F "QUANTITYORDERED=30" \
  -F "PRICEEACH=95.70" \
  -F "ORDERLINENUMBER=2" \
  -F "SALES=2871" \
  -F "ORDERDATE=24/02/2018" \
  -F "DAYS_SINCE_LASTORDER=828" \
  -F "STATUS=Shipped" \
  -F "PRODUCTLINE=Motorcycles" \
  -F "MSRP=95" \
  -F "PRODUCTCODE=S10_1678" \
  -F "CUSTOMERNAME=Land of Toys Inc." \
  -F "PHONE=2125557818" \
  -F "ADDRESSLINE1=897 Long Airport Avenue" \
  -F "CITY=NYC" \
  -F "POSTALCODE=10022" \
  -F "COUNTRY=USA" \
  -F "CONTACTLASTNAME=Yu" \
  -F "CONTACTFIRSTNAME=Kwai" \
  -F "DEALSIZE=Small"
```

## Development

### Adding New Features
- API endpoints are defined in `main.py`
- HTML templates are in the `templates/` directory
- Static assets go in the `static/` directory
- Follow the patterns established for consistent UI/UX

### Data Storage
Currently uses CSV files for simplicity. To upgrade to a database:
1. Replace `get_dataframe()` and `save_dataframe()` functions
2. Add database models and connection logic
3. Update the requirements.txt with database drivers

### Customization
- Modify the sample data generation in `get_dataframe()`
- Add new fields by updating the data model and templates
- Extend the analysis features in the `/api/analyze` endpoint
- Customize the UI styling in `static/css/style.css`
