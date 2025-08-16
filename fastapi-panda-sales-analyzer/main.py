from fastapi import FastAPI, HTTPException, Request, Form, Query, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from services.data_service import DataService
import uvicorn
import os
from datetime import datetime

app = FastAPI(title='Sales Analyzer')

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.getenv('DATA_FILE', os.path.join(BASE_DIR, 'data', 'sample_data.csv'))

app.mount('/static', StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name='static')
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

service = DataService(DATA_FILE)


class RecordModel(BaseModel):
    # Generic model allowing additional keys
    ORDERNUMBER: Optional[int] = Field(None)
    QUANTITYORDERED: Optional[int] = Field(None)
    PRICEEACH: Optional[float] = Field(None)
    ORDERLINENUMBER: Optional[int] = Field(None)
    SALES: Optional[float] = Field(None)
    ORDERDATE: Optional[str] = Field(None)
    DAYS_SINCE_LASTORDER: Optional[int] = Field(None)
    STATUS: Optional[str] = Field(None)
    PRODUCTLINE: Optional[str] = Field(None)
    MSRP: Optional[float] = Field(None)
    PRODUCTCODE: Optional[str] = Field(None)
    CUSTOMERNAME: Optional[str] = Field(None)
    PHONE: Optional[str] = Field(None)
    ADDRESSLINE1: Optional[str] = Field(None)
    CITY: Optional[str] = Field(None)
    POSTALCODE: Optional[str] = Field(None)
    COUNTRY: Optional[str] = Field(None)
    CONTACTLASTNAME: Optional[str] = Field(None)
    CONTACTFIRSTNAME: Optional[str] = Field(None)
    DEALSIZE: Optional[str] = Field(None)

    class Config:
        extra = 'allow'


class AddRecordModel(RecordModel):
    ORDERDATE: Optional[str] = None

    @validator('PRICEEACH', 'SALES', 'MSRP', pre=True, always=False)
    def numeric_positive(cls, v):
        if v is None or v == '':
            return v
        try:
            val = float(v)
        except Exception:
            raise ValueError('Must be a number')
        if val < 0:
            raise ValueError('Must be non-negative')
        return val

    @validator('ORDERDATE', pre=True, always=False)
    def parse_date(cls, v):
        if v is None or v == '':
            return v
        for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%m/%d/%Y'):
            try:
                d = datetime.strptime(v, fmt)
                return d.strftime('%Y-%m-%d')
            except Exception:
                continue
        raise ValueError('ORDERDATE must be a valid date (d/m/Y or Y-m-d)')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    summary = service.analyze()
    rows = service.get_rows(limit=10)
    return templates.TemplateResponse('index.html', {'request': request, 'summary': summary, 'rows': rows})


@app.get('/add', response_class=HTMLResponse)
async def add_form(request: Request):
    return templates.TemplateResponse('add.html', {'request': request})


@app.post('/add')
async def add_post(request: Request, ORDERNUMBER: int = Form(...), QUANTITYORDERED: int = Form(...), PRICEEACH: float = Form(...)):
    # Collect remaining optional form fields
    form = await request.form()
    record = {k: v for k, v in form.items()}
    try:
        new_id = service.add_record(record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return RedirectResponse(url='/', status_code=303)


@app.get('/edit/{record_id}', response_class=HTMLResponse)
async def edit_form(request: Request, record_id: int):
    rec = service.get_record(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail='Record not found')
    return templates.TemplateResponse('edit.html', {'request': request, 'record': rec})


@app.post('/edit/{record_id}')
async def edit_post(record_id: int, request: Request):
    form = await request.form()
    updates = {k: v for k, v in form.items()}
    ok = service.update_record(record_id, updates)
    if not ok:
        raise HTTPException(status_code=404, detail='Record not found')
    return RedirectResponse(url='/', status_code=303)


# API endpoints
@app.get('/api/analyze')
async def api_analyze():
    return service.analyze()


@app.get('/api/data')
async def api_get_data(position: Optional[str] = Query('top', regex='^(top|bottom)$'), limit: int = Query(10, ge=1, le=100), sort_by: Optional[str] = None, ascending: bool = False):
    # position controls whether to return top or bottom rows
    if position == 'bottom':
        rows = service.get_rows(limit=limit, sort_by=sort_by, ascending=False)
        # to get bottom rows, reverse the ascending flag
        rows = list(reversed(rows))
        return rows
    return service.get_rows(limit=limit, sort_by=sort_by, ascending=True)


@app.post('/api/data')
async def api_post_data(record: RecordModel):
    new_id = service.add_record(record.dict(exclude_none=True))
    return {'id': new_id}


@app.put('/api/data/{record_id}')
async def api_put_data(record_id: int, updates: Dict[str, Any]):
    ok = service.update_record(record_id, updates)
    if not ok:
        raise HTTPException(status_code=404, detail='Record not found')
    return {'ok': True}


@app.delete('/api/data/{record_id}')
async def api_delete_data(record_id: int):
    ok = service.delete_record(record_id)
    if not ok:
        raise HTTPException(status_code=404, detail='Record not found')
    return {'ok': True}


# Data cleaning endpoints
@app.post('/api/clean/drop_duplicates')
async def api_drop_duplicates(columns: Optional[str] = Form(None)):
    subset = columns.split(',') if columns else None
    removed = service.drop_duplicates(subset=subset)
    return {'removed': removed}


@app.get('/api/clean/duplicates')
async def api_get_duplicates(columns: Optional[str] = Query(None)):
    subset = columns.split(',') if columns else None
    dup = service.get_duplicates(subset=subset)
    return {'duplicates': dup}


@app.post('/api/clean/fill_missing')
async def api_fill_missing(column: str = Form(...), value: str = Form(...)):
    count = service.fill_missing(column, value)
    return {'filled': count}


@app.post('/api/clean/coerce')
async def api_coerce(column: str = Form(...), dtype: str = Form(...)):
    ok = service.coerce_column_type(column, dtype)
    return {'ok': ok}


@app.get('/data_cleaning', response_class=HTMLResponse)
async def data_cleaning(request: Request):
    return templates.TemplateResponse('data_cleaning.html', {'request': request})


@app.get('/data_cleaning/duplicates', response_class=HTMLResponse)
async def data_cleaning_duplicates(request: Request, columns: Optional[str] = None):
    subset = columns.split(',') if columns else None
    dup = service.get_duplicates(subset=subset)
    return templates.TemplateResponse('data_cleaning.html', {'request': request, 'duplicates': dup})


@app.post('/data_cleaning/drop_duplicates')
async def data_cleaning_drop(request: Request, columns: Optional[str] = Form(None)):
    subset = columns.split(',') if columns else None
    removed = service.drop_duplicates(subset=subset)
    return RedirectResponse(url='/data_cleaning', status_code=303)


@app.post('/data_cleaning/fill_missing')
async def data_cleaning_fill(request: Request, column: str = Form(...), value: str = Form('')):
    count = service.fill_missing(column, value)
    return RedirectResponse(url='/data_cleaning', status_code=303)


@app.post('/data_cleaning/coerce')
async def data_cleaning_coerce(request: Request, column: str = Form(...), dtype: str = Form(...)):
    ok = service.coerce_column_type(column, dtype)
    return RedirectResponse(url='/data_cleaning', status_code=303)


@app.get('/api/chart/productline')
async def api_chart_productline():
    return service.aggregate_sales_by_productline()


@app.get('/api/chart/sales_over_time')
async def api_chart_sales_over_time(freq: str = Query('M')):
    # validate freq to prevent abuse
    if freq not in {'D', 'W', 'M', 'Y'}:
        raise HTTPException(status_code=400, detail='freq must be one of D,W,M,Y')
    return service.sales_over_time(freq=freq)


# Update the add endpoint to validate using AddRecordModel
@app.post('/api/data/validated')
async def api_post_data_validated(record: AddRecordModel):
    payload = record.dict(exclude_none=True)
    new_id = service.add_record(payload)
    return {'id': new_id}


@app.get('/health')
async def health():
    """Simple health check for load balancers / Cloud Run readiness."""
    return {"status": "ok"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
