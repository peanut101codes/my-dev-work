# Car Sales Data Analyzer

A small data analysis web app built with FastAPI, Pandas, and Jinja2 to explore and clean a car sales dataset. The app displays the top records, renders visualizations by default on the home page, allows data cleaning operations, and accepts new record submissions which are appended to the CSV dataset.

## Features

- Display the top 10 rows of the dataset on the home page
- Default visualizations: sales over time, price distribution, car make popularity, sales by country
- Data cleaning operations: handle missing values, remove duplicates, standardize text, remove outliers
- Submit new car sales records via a form (appends to the CSV file)
- Uses Jinja2 templates to render pages and static images for charts

## Project structure

```
project/
│
├── app/
│   ├── main.py           # FastAPI app initialization and routes
│   ├── models.py         # Pydantic models for data validation
│   ├── crud/             # CRUD operations (data cleaning, visualizations, data submission)
│   │   ├── data_cleaning.py  # Logic for cleaning the dataset
│   │   ├── visualizations.py  # Logic for generating visualizations
│   │   └── data_submission.py  # Logic for submitting a new record
│   ├── schemas/          # Request/Response models
│   │   ├── data_cleaning.py
│   │   ├── visualizations.py
│   │   └── data_submission.py
│   ├── static/           # Static files (e.g., generated charts)
│   └── templates/        # Jinja2 templates for frontend
│
├── data/                 # Car sales dataset (e.g., car_sales.csv)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Installation

1. Create and activate a Python virtual environment (recommended):

   python -m venv .venv
   source .venv/bin/activate (mac) or source .venv/Scripts/activate (windows)

2. Install dependencies:

   pip install -r requirements.txt

## Running the app

Start the development server with Uvicorn:

   uvicorn app.main:app --reload

Open the app in your browser at http://localhost:8000

## Routes / Endpoints

- `/` (GET) — Home page: displays top 10 records and default visualizations
- `/visualizations` (GET) — Returns visualization images or HTML to embed the charts
- `/clean-data` (POST) — Apply data cleaning operations (fill/drop missing, remove duplicates, standardize text, remove outliers)
- `/submit-record` (POST) — Submit a new record via a form; appends to the CSV dataset

## Data handling

- The dataset is stored in `data/car_sales.csv` (or similar). Pandas is used to read, process, and write the CSV.
- After cleaning operations, save updates back to the CSV file.
- When a new record is submitted, append it to the CSV.

## Visualizations

- Use Matplotlib or Seaborn to generate charts:
  - Line plot for sales over time
  - Histogram / box plot for price distribution
  - Bar chart for car make popularity
  - Bar chart (or map) for sales by country
- Save charts as static images in `app/static/` and reference them from templates.

## Templates

- Jinja2 templates in `app/templates/` render the home page and the submission form.


For more detailed Copilot-oriented development instructions, see `COPILOT_INSTRUCTIONS.md` in the project root.
