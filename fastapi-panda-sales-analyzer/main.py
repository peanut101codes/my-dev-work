from fastapi import FastAPI, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from pathlib import Path
import uvicorn
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import io
import base64

# Initialize FastAPI app
app = FastAPI(title="Data Analysis API", version="1.0.0")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sample dataset - In production, this would come from a database
DATA_FILE = "data/sample_data.csv"

def get_dataframe():
    """Load the dataset from CSV file"""
    try:
        df = pd.read_csv(DATA_FILE)
        # Convert ORDERDATE to datetime if it exists
        if 'ORDERDATE' in df.columns:
            df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], format='%d/%m/%Y', errors='coerce')
        return df
    except FileNotFoundError:
        # Create sample sales data if file doesn't exist
        sample_data = {
            'ORDERNUMBER': range(10001, 10101),
            'QUANTITYORDERED': np.random.randint(10, 50, 100),
            'PRICEEACH': np.random.uniform(50, 200, 100).round(2),
            'ORDERLINENUMBER': np.random.randint(1, 10, 100),
            'SALES': np.random.uniform(500, 5000, 100).round(2),
            'ORDERDATE': pd.date_range('2018-01-01', periods=100, freq='D'),
            'DAYS_SINCE_LASTORDER': np.random.randint(1, 365, 100),
            'STATUS': np.random.choice(['Shipped', 'Processing', 'Disputed', 'Cancelled'], 100),
            'PRODUCTLINE': np.random.choice(['Motorcycles', 'Classic Cars', 'Trucks', 'Vintage Cars'], 100),
            'MSRP': np.random.randint(50, 300, 100),
            'PRODUCTCODE': [f'S{10+i}_{1000+i}' for i in range(100)],
            'CUSTOMERNAME': [f'Customer_{i}' for i in range(1, 101)],
            'PHONE': [f'555-{1000+i}' for i in range(100)],
            'ADDRESSLINE1': [f'{1000+i} Main Street' for i in range(100)],
            'CITY': np.random.choice(['NYC', 'Los Angeles', 'Chicago', 'Houston'], 100),
            'POSTALCODE': np.random.randint(10000, 99999, 100),
            'COUNTRY': np.random.choice(['USA', 'Canada', 'UK', 'France'], 100),
            'CONTACTLASTNAME': [f'LastName_{i}' for i in range(100)],
            'CONTACTFIRSTNAME': [f'FirstName_{i}' for i in range(100)],
            'DEALSIZE': np.random.choice(['Small', 'Medium', 'Large'], 100)
        }
        df = pd.DataFrame(sample_data)
        # Ensure data directory exists
        Path("data").mkdir(exist_ok=True)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_dataframe(df):
    """Save the dataframe to CSV file"""
    Path("data").mkdir(exist_ok=True)
    df.to_csv(DATA_FILE, index=False)

def create_plot_response(fig):
    """Convert matplotlib figure to HTTP response"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
    img_buffer.seek(0)
    plt.close(fig)
    return StreamingResponse(io.BytesIO(img_buffer.read()), media_type="image/png")

def create_base64_plot(fig):
    """Convert matplotlib figure to base64 string for embedding"""
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=300)
    img_buffer.seek(0)
    plot_data = img_buffer.getvalue()
    plt.close(fig)
    return base64.b64encode(plot_data).decode()

def create_sales_trends_plot(df):
    """Create sales trends over time plot"""
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Group by month and sum sales
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'], errors='coerce')
    monthly_sales = df.groupby(df['ORDERDATE'].dt.to_period('M'))['SALES'].sum()
    
    ax.plot(monthly_sales.index.astype(str), monthly_sales.values, marker='o', linewidth=3, markersize=8)
    ax.set_title('Sales Trends Over Time', fontsize=20, fontweight='bold', pad=20)
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Total Sales ($)', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    # Format y-axis to show currency
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    
    return fig

def create_product_line_analysis(df):
    """Create product line analysis plots"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    
    # 1. Sales by Product Line
    product_sales = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    ax1.bar(product_sales.index, product_sales.values, color=colors[:len(product_sales)])
    ax1.set_title('Total Sales by Product Line', fontweight='bold', fontsize=16)
    ax1.set_ylabel('Sales ($)', fontsize=12)
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=11)
    ax1.tick_params(axis='y', labelsize=11)
    
    # 2. Average Order Value by Product Line
    avg_order = df.groupby('PRODUCTLINE')['SALES'].mean().sort_values(ascending=False)
    ax2.bar(avg_order.index, avg_order.values, color=colors[:len(avg_order)])
    ax2.set_title('Average Order Value by Product Line', fontweight='bold', fontsize=16)
    ax2.set_ylabel('Average Order Value ($)', fontsize=12)
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right', fontsize=11)
    ax2.tick_params(axis='y', labelsize=11)
    
    # 3. Quantity Distribution
    product_qty = df.groupby('PRODUCTLINE')['QUANTITYORDERED'].sum().sort_values(ascending=False)
    ax3.bar(product_qty.index, product_qty.values, color=colors[:len(product_qty)])
    ax3.set_title('Total Quantity Ordered by Product Line', fontweight='bold', fontsize=16)
    ax3.set_ylabel('Quantity Ordered', fontsize=12)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha='right', fontsize=11)
    ax3.tick_params(axis='y', labelsize=11)
    
    # 4. Product Line Performance (Sales vs Quantity)
    perf_data = df.groupby('PRODUCTLINE').agg({
        'SALES': 'sum',
        'QUANTITYORDERED': 'sum'
    }).reset_index()
    
    scatter = ax4.scatter(perf_data['QUANTITYORDERED'], perf_data['SALES'], 
                         s=150, alpha=0.7, c=range(len(perf_data)), cmap='viridis')
    
    for i, txt in enumerate(perf_data['PRODUCTLINE']):
        ax4.annotate(txt, (perf_data['QUANTITYORDERED'].iloc[i], perf_data['SALES'].iloc[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    ax4.set_title('Sales vs Quantity by Product Line', fontweight='bold', fontsize=16)
    ax4.set_xlabel('Total Quantity Ordered', fontsize=12)
    ax4.set_ylabel('Total Sales ($)', fontsize=12)
    ax4.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax4.tick_params(axis='both', labelsize=11)
    
    plt.tight_layout(pad=3.0)
    return fig

def create_geographic_analysis(df):
    """Create geographic sales analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))
    
    # 1. Top 10 Countries by Sales
    country_sales = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False).head(10)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
    
    bars = ax1.barh(country_sales.index, country_sales.values, color=colors[:len(country_sales)], height=0.6)
    ax1.set_title('Top 10 Countries by Sales', fontweight='bold', fontsize=18, pad=20)
    ax1.set_xlabel('Total Sales ($)', fontsize=14, fontweight='bold')
    ax1.xaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.tick_params(axis='x', labelsize=12)
    ax1.tick_params(axis='y', labelsize=13)
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars with better positioning
    for bar in bars:
        width = bar.get_width()
        ax1.text(width + max(country_sales) * 0.01, bar.get_y() + bar.get_height()/2, 
                f'${width:,.0f}', ha='left', va='center', fontsize=11, fontweight='bold')
    
    # Set x-axis limit to accommodate labels
    ax1.set_xlim(0, max(country_sales) * 1.15)
    
    # 2. Sales Distribution by Deal Size - Enhanced pie chart
    deal_sales = df.groupby('DEALSIZE')['SALES'].sum()
    deal_percentages = (deal_sales / deal_sales.sum() * 100).round(1)
    
    # Create custom labels with values and percentages
    labels = [f'{size}\n${value:,.0f}\n({pct}%)' 
              for size, value, pct in zip(deal_sales.index, deal_sales.values, deal_percentages)]    
    
    ax2.set_title('Sales Distribution by Deal Size', fontweight='bold', fontsize=18, pad=20)
    
    # Add total sales in center
    total_sales = deal_sales.sum()
    ax2.text(0, 0, f'Total Sales\n${total_sales:,.0f}', ha='center', va='center', 
             fontsize=14, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout(pad=4.0)
    return fig

def create_order_status_analysis(df):
    """Create order status and performance analysis"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(22, 18))
    
    # 1. Order Status Distribution - Enhanced pie chart
    status_counts = df['STATUS'].value_counts()
    status_percentages = (status_counts / status_counts.sum() * 100).round(1)
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6', '#9b59b6']
    
    # Create custom labels with counts and percentages
    labels = [f'{status}\n{count} orders\n({pct}%)' 
              for status, count, pct in zip(status_counts.index, status_counts.values, status_percentages)]
    
    ax1.set_title('Order Status Distribution', fontweight='bold', fontsize=18, pad=20)
    
    # Add total orders in center
    total_orders = status_counts.sum()
    ax1.text(0, 0, f'Total Orders\n{total_orders:,}', ha='center', va='center', 
             fontsize=13, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9))
    
    # 2. Sales by Order Status - Enhanced bar chart
    status_sales = df.groupby('STATUS')['SALES'].sum().sort_values(ascending=False)
    bars = ax2.bar(status_sales.index, status_sales.values, color=colors[:len(status_sales)], 
                   width=0.6, edgecolor='black', linewidth=1)
    ax2.set_title('Total Sales by Order Status', fontweight='bold', fontsize=18, pad=20)
    ax2.set_ylabel('Sales ($)', fontsize=14, fontweight='bold')
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax2.tick_params(axis='x', labelsize=12, rotation=0)
    ax2.tick_params(axis='y', labelsize=12)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(status_sales) * 0.01,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 3. Price Distribution - Enhanced histogram
    ax3.hist(df['PRICEEACH'], bins=25, alpha=0.8, color='skyblue', edgecolor='navy', linewidth=1)
    ax3.set_title('Price Distribution', fontweight='bold', fontsize=18, pad=20)
    ax3.set_xlabel('Price Each ($)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Frequency', fontsize=14, fontweight='bold')
    ax3.tick_params(axis='both', labelsize=12)
    ax3.grid(axis='y', alpha=0.3)
    
    # Add statistics
    mean_price = df['PRICEEACH'].mean()
    median_price = df['PRICEEACH'].median()
    ax3.axvline(mean_price, color='red', linestyle='--', linewidth=3,
               label=f'Mean: ${mean_price:.2f}')
    ax3.axvline(median_price, color='orange', linestyle='--', linewidth=3,
               label=f'Median: ${median_price:.2f}')
    ax3.legend(fontsize=12, loc='upper right')
    
    # 4. Sales vs Quantity Correlation - Enhanced scatter plot
    scatter = ax4.scatter(df['QUANTITYORDERED'], df['SALES'], alpha=0.6, 
                         c=df['QUANTITYORDERED'], cmap='viridis', s=30, edgecolors='black', linewidth=0.5)
    ax4.set_title('Sales vs Quantity Ordered', fontweight='bold', fontsize=18, pad=20)
    ax4.set_xlabel('Quantity Ordered', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Sales ($)', fontsize=14, fontweight='bold')
    ax4.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax4.tick_params(axis='both', labelsize=12)
    ax4.grid(alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Quantity Ordered', fontsize=12, fontweight='bold')
    
    # Add correlation coefficient with enhanced styling
    correlation = df['QUANTITYORDERED'].corr(df['SALES'])
    ax4.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
            transform=ax4.transAxes, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8),
            fontsize=14, fontweight='bold')
    
    # Add trend line
    z = np.polyfit(df['QUANTITYORDERED'], df['SALES'], 1)
    p = np.poly1d(z)
    ax4.plot(df['QUANTITYORDERED'], p(df['QUANTITYORDERED']), "r--", alpha=0.8, linewidth=2)
    
    plt.tight_layout(pad=4.0)
    return fig

# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with data visualization"""
    df = get_dataframe()
    
    # Basic statistics for the frontend
    stats = {
        'total_records': len(df),
        'columns': df.columns.tolist(),
        'numeric_summary': df.select_dtypes(include=[np.number]).describe().to_dict(),
        'total_sales': df['SALES'].sum() if 'SALES' in df.columns else 0,
        'avg_order_value': df['SALES'].mean() if 'SALES' in df.columns else 0,
        'product_line_counts': df['PRODUCTLINE'].value_counts().to_dict() if 'PRODUCTLINE' in df.columns else {},
        'status_counts': df['STATUS'].value_counts().to_dict() if 'STATUS' in df.columns else {},
        'country_counts': df['COUNTRY'].value_counts().to_dict() if 'COUNTRY' in df.columns else {},
        'deal_size_counts': df['DEALSIZE'].value_counts().to_dict() if 'DEALSIZE' in df.columns else {}
    }
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stats": stats,
        "data": df.head(10).to_dict('records')
    })

@app.get("/api/analyze")
async def analyze_dataset():
    """GET endpoint to analyze dataset and return summary"""
    df = get_dataframe()
    
    analysis = {
        "dataset_info": {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        },
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "numeric_summary": {},
        "categorical_summary": {}
    }
    
    # Numeric column analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        analysis["numeric_summary"] = df[numeric_cols].describe().to_dict()
    
    # Categorical column analysis
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        analysis["categorical_summary"][col] = {
            "unique_values": df[col].nunique(),
            "most_frequent": df[col].mode().iloc[0] if not df[col].empty else None,
            "value_counts": df[col].value_counts().head(5).to_dict()
        }
    
    return analysis

@app.get("/api/charts/sales-trends")
async def get_sales_trends_chart():
    """Generate sales trends chart"""
    try:
        df = get_dataframe()
        if df.empty:
            return {"error": "No data available"}
        
        fig = create_sales_trends_plot(df)
        
        # Save to BytesIO buffer
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return StreamingResponse(img_buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/charts/product-analysis")
async def get_product_analysis_chart():
    """Generate product line analysis chart"""
    try:
        df = get_dataframe()
        if df.empty:
            return {"error": "No data available"}
        
        fig = create_product_line_analysis(df)
        
        # Save to BytesIO buffer
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return StreamingResponse(img_buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/charts/geographic-analysis")
async def get_geographic_analysis_chart():
    """Generate geographic analysis chart"""
    try:
        df = get_dataframe()
        if df.empty:
            return {"error": "No data available"}
        
        fig = create_geographic_analysis(df)
        
        # Save to BytesIO buffer
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return StreamingResponse(img_buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/charts/order-status")
async def get_order_status_chart():
    """Generate order status analysis chart"""
    try:
        df = get_dataframe()
        if df.empty:
            return {"error": "No data available"}
        
        fig = create_order_status_analysis(df)
        
        # Save to BytesIO buffer
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=200, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)
        
        return StreamingResponse(img_buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/data")
async def get_data(
    position: str = Query("top", description="'top' for first rows, 'bottom' for last rows"),
    limit: int = Query(10, description="Number of rows to return", ge=1, le=100)
):
    """GET endpoint to return top or bottom rows based on query parameters"""
    df = get_dataframe()
    
    if position.lower() == "top":
        result_df = df.head(limit)
    elif position.lower() == "bottom":
        result_df = df.tail(limit)
    else:
        raise HTTPException(status_code=400, detail="Position must be 'top' or 'bottom'")
    
    return {
        "position": position,
        "limit": limit,
        "total_records": len(df),
        "data": result_df.to_dict('records')
    }

@app.post("/api/data")
async def add_record(
    ordernumber: int = Form(...),
    quantityordered: int = Form(...),
    priceeach: float = Form(...),
    sales: float = Form(...),
    orderdate: str = Form(...),
    status: str = Form(...),
    productline: str = Form(...),
    customername: str = Form(...),
    phone: str = Form(...),
    city: str = Form(...),
    country: str = Form(...),
    dealsize: str = Form(...)
):
    """POST endpoint to add a new record"""
    df = get_dataframe()
    
    # Create new record
    new_record = {
        'ORDERNUMBER': ordernumber,
        'QUANTITYORDERED': quantityordered,
        'PRICEEACH': priceeach,
        'ORDERLINENUMBER': 1,  # Default value
        'SALES': sales,
        'ORDERDATE': orderdate,
        'DAYS_SINCE_LASTORDER': 0,  # Default value
        'STATUS': status,
        'PRODUCTLINE': productline,
        'MSRP': priceeach * 1.2,  # Default markup
        'PRODUCTCODE': f'P{ordernumber}',
        'CUSTOMERNAME': customername,
        'PHONE': phone,
        'ADDRESSLINE1': 'Address TBD',
        'CITY': city,
        'POSTALCODE': '00000',
        'COUNTRY': country,
        'CONTACTLASTNAME': 'TBD',
        'CONTACTFIRSTNAME': 'TBD',
        'DEALSIZE': dealsize
    }
    
    # Add to dataframe
    new_df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
    save_dataframe(new_df)
    
    return {
        "message": "Record added successfully",
        "record": new_record
    }

@app.put("/api/data/{record_id}")
async def update_record(
    record_id: int,
    ordernumber: int = Form(...),
    quantityordered: int = Form(...),
    priceeach: float = Form(...),
    sales: float = Form(...),
    orderdate: str = Form(...),
    status: str = Form(...),
    productline: str = Form(...),
    customername: str = Form(...),
    phone: str = Form(...),
    city: str = Form(...),
    country: str = Form(...),
    dealsize: str = Form(...)
):
    """PUT endpoint to edit an existing record"""
    df = get_dataframe()
    
    # Check if record exists
    if record_id not in df['ORDERNUMBER'].values:
        raise HTTPException(status_code=404, detail=f"Record with Order Number {record_id} not found")
    
    # Update the record
    mask = df['ORDERNUMBER'] == record_id
    df.loc[mask, 'ORDERNUMBER'] = ordernumber
    df.loc[mask, 'QUANTITYORDERED'] = quantityordered
    df.loc[mask, 'PRICEEACH'] = priceeach
    df.loc[mask, 'SALES'] = sales
    df.loc[mask, 'ORDERDATE'] = orderdate
    df.loc[mask, 'STATUS'] = status
    df.loc[mask, 'PRODUCTLINE'] = productline
    df.loc[mask, 'CUSTOMERNAME'] = customername
    df.loc[mask, 'PHONE'] = phone
    df.loc[mask, 'CITY'] = city
    df.loc[mask, 'COUNTRY'] = country
    df.loc[mask, 'DEALSIZE'] = dealsize
    
    save_dataframe(df)
    
    updated_record = df[mask].iloc[0].to_dict()
    
    return {
        "message": "Record updated successfully",
        "record": updated_record
    }

@app.delete("/api/data/{record_id}")
async def delete_record(record_id: int):
    """DELETE endpoint to remove a record"""
    df = get_dataframe()
    
    # Check if record exists
    if record_id not in df['ORDERNUMBER'].values:
        raise HTTPException(status_code=404, detail=f"Record with Order Number {record_id} not found")
    
    # Remove the record
    df = df[df['ORDERNUMBER'] != record_id]
    save_dataframe(df)
    
    return {
        "message": f"Record with Order Number {record_id} deleted successfully"
    }

# Frontend routes for forms

@app.get("/add", response_class=HTMLResponse)
async def add_form(request: Request):
    """Form to add new record"""
    return templates.TemplateResponse("add_record.html", {"request": request})

@app.get("/edit/{record_id}", response_class=HTMLResponse)
async def edit_form(request: Request, record_id: int):
    """Form to edit existing record"""
    df = get_dataframe()
    
    if record_id not in df['ORDERNUMBER'].values:
        raise HTTPException(status_code=404, detail=f"Record with Order Number {record_id} not found")
    
    record = df[df['ORDERNUMBER'] == record_id].iloc[0].to_dict()
    
    return templates.TemplateResponse("edit_record.html", {
        "request": request,
        "record": record
    })

@app.get("/data_cleaning", response_class=HTMLResponse)
async def data_cleaning(request: Request):
    """Data cleaning interface"""
    df = get_dataframe()
    
    # Analysis for data cleaning
    cleaning_info = {
        'missing_values': df.isnull().sum().to_dict(),
        'duplicates': df.duplicated().sum(),
        'data_types': df.dtypes.astype(str).to_dict(),
        'sample_data': df.head(10).to_dict('records')
    }
    
    return templates.TemplateResponse("data_cleaning.html", {
        "request": request,
        "cleaning_info": cleaning_info
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
