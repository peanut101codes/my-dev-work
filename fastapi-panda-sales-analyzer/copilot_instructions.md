Great choice! Displaying the visualizations by default will give users immediate insights when they access the page, and they can dive deeper into specific data cleaning or further analysis if needed.

### Now, I have enough information to draft the `copilot-instruction.md` file. Here's a guide that outlines the functionality, structure, and key points for your project.

---

## Copilot Instruction: Car Sales Data Analyzer

### Overview

This project is a data analysis tool built with FastAPI, Pandas, and Jinja2. It allows users to explore and clean a car sales dataset. Users can view the top 10 records, visualize various trends, clean the data, and submit new records. The data is stored in a CSV file, and visualizations are displayed by default.

### Project Structure

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

### Functionality

#### 1. **Displaying the Top 10 Records**

* On the home page, display the first 10 rows of the dataset in a user-friendly table.
* Each record should have the car details like make, model, price, year, etc.
* **Route**: `/`
* **Method**: `GET`
* **Dependencies**: `pandas` for data handling

#### 2. **Visualizations (Displayed by Default)**

The following charts will be displayed by default on the home page:

* **Sales Over Time**: A time-series plot of sales trends.

* **Price Distribution**: A histogram or box plot for car price distribution.

* **Car Make Popularity**: A bar chart showing the number of cars sold for each make.

* **Sales by Country**: A bar chart (or map) of sales distribution by country.

* **Route**: `/visualizations`

* **Method**: `GET`

* **Dependencies**: `matplotlib` / `seaborn` for plotting

#### 3. **Data Cleaning**

Provide users with the option to clean the data through the following operations:

* **Handling Missing Values**: Users can choose to fill or drop missing values.

* **Removing Duplicates**: Automatically identify and remove duplicate records.

* **Standardizing Text**: Normalize text fields (e.g., lowercase, trim whitespace).

* **Outlier Removal**: Optionally, remove records with extreme values (e.g., car prices outside a reasonable range).

* **Route**: `/clean-data`

* **Method**: `POST`

* **Dependencies**: `pandas` for data manipulation

#### 4. **Submitting a New Record**

Users can submit a new car sales record via a form. The form will collect the following fields:

* Car make, model, price, year, country, etc.

Upon submission, the record will be added directly to the CSV file, and the dataset will be updated.

* **Route**: `/submit-record`
* **Method**: `POST`
* **Form Fields**: Car make, model, price, year, country, etc.
* **Dependencies**: `pandas` for appending data to CSV

---

### Detailed Instructions

#### FastAPI Setup (main.py)

* **App Initialization**: Set up FastAPI and define routes for:

  * Home page (displays the top 10 records)
  * Visualizations page
  * Data cleaning operations
  * Data submission form
* **CRUD Operations**:

  * Implement functions for data cleaning and visualizations in `crud/data_cleaning.py` and `crud/visualizations.py`.
  * Write functions to handle the form submission in `crud/data_submission.py`.

#### Data Handling (pandas)

* Use **Pandas** for reading, processing, and cleaning the dataset.
* After submitting a new record, **append** the data to the CSV file.
* After cleaning the data (e.g., removing duplicates), save the updated dataset back to the CSV.

#### Data Visualizations (matplotlib / seaborn)

* Use **matplotlib** or **seaborn** to generate:

  * Line plot for sales over time
  * Histogram for price distribution
  * Bar chart for car make popularity
  * Bar chart (or map) for sales by country
* Render these visualizations as static images and display them on the home page.

#### Templates (Jinja2)

* Use **Jinja2** templates to render HTML for the home page and form submission page.
* The home page should display the top 10 records and visualizations.
* The submission page should include a form to allow users to submit new records.

---

### Dependencies

* **FastAPI**: For the web framework.
* **Pandas**: For data manipulation and analysis.
* **Matplotlib / Seaborn**: For visualizations.
* **Jinja2**: For HTML templating.

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

### Running the App

To run the app, use the following command:

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI server and you can access the app in your browser at `http://localhost:8000`.

---

Let me know if you’d like any changes or additional details!
