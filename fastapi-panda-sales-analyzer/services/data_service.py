import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


class DataService:
    """CSV-backed data service with simple concurrency control and cleaning utilities.

    - Writes are atomic (write to temp file then os.replace).
    - Provides analysis, CRUD and basic data-cleaning helpers.
    """

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        # ensure file exists
        if not self.csv_path.exists():
            pd.DataFrame().to_csv(self.csv_path, index=False)

    def _read_df(self) -> pd.DataFrame:
        """Read CSV into DataFrame. No file locking (cooperative single-process expected).

        Note: removing advisory locks for simpler deployment; consider a DB for
        concurrent access in production.
        """
        # Let pandas infer types; caller may coerce later
        df = pd.read_csv(self.csv_path)
        # Ensure an `id` column exists and is integer when possible
        if 'id' not in df.columns:
            df = df.reset_index().rename(columns={'index': 'id'})
        if not df.empty:
            try:
                df['id'] = df['id'].astype(int)
            except Exception:
                # leave as-is if coercion fails
                pass
        return df

    def _write_df(self, df: pd.DataFrame) -> None:
        """Atomically write DataFrame to CSV."""
        # write to a temp file in the same directory and then replace
        fd, tmp = tempfile.mkstemp(dir=str(self.csv_path.parent))
        os.close(fd)
        try:
            df.to_csv(tmp, index=False)
            os.replace(tmp, self.csv_path)
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

    def get_columns(self) -> List[str]:
        df = self._read_df()
        return list(df.columns)

    def analyze(self) -> Dict[str, Any]:
        df = self._read_df()
        result: Dict[str, Any] = {}
        result['rows'] = int(df.shape[0])
        result['columns'] = list(df.columns)
        result['dtypes'] = {c: str(dtype) for c, dtype in df.dtypes.items()}
        result['missing'] = {c: int(df[c].isna().sum()) for c in df.columns}
        numeric = df.select_dtypes(include='number')
        if not numeric.empty:
            result['numeric_summary'] = numeric.describe().to_dict()
        else:
            result['numeric_summary'] = {}
        return result

    def get_rows(self, limit: int = 10, sort_by: Optional[str] = None, ascending: bool = False) -> List[Dict[str, Any]]:
        df = self._read_df()
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by, ascending=ascending)
        else:
            if 'id' in df.columns:
                df = df.sort_values(by='id', ascending=ascending)
        head = df.head(limit)
        return head.fillna('').to_dict(orient='records')  # type: ignore[return-value]

    def add_record(self, record: Dict[str, Any]) -> int:
        df = self._read_df()
        # Determine next id safely
        if 'id' in df.columns and not df.empty:
            try:
                next_id = int(df['id'].max()) + 1
            except Exception:
                next_id = 1
        else:
            next_id = 1
        record_copy = {k: v for k, v in record.items()}
        record_copy['id'] = next_id
        # Ensure columns align: add missing columns to df
        if df.empty:
            df = pd.DataFrame([record_copy])
        else:
            # append via concat to avoid deprecated append
            new_row = pd.DataFrame([record_copy])
            # reindex new_row to include missing columns (union)
            df = pd.concat([df, new_row], ignore_index=True, sort=False)
        self._write_df(df)
        return next_id

    def update_record(self, record_id: int, updates: Dict[str, Any]) -> bool:
        df = self._read_df()
        if 'id' not in df.columns:
            return False
        mask = df['id'] == int(record_id)
        if not mask.any():
            return False
        # ensure all update columns exist
        for k in updates.keys():
            if k not in df.columns and k != 'id':
                df[k] = pd.NA
        for k, v in updates.items():
            if k == 'id':
                continue
            df.loc[mask, k] = v
        self._write_df(df)
        return True

    def delete_record(self, record_id: int) -> bool:
        df = self._read_df()
        if 'id' not in df.columns:
            return False
        orig_len = len(df)
        df = df[df['id'] != int(record_id)]
        if len(df) == orig_len:
            return False
        self._write_df(df)
        return True

    def get_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        df = self._read_df()
        if 'id' not in df.columns:
            return None
        row = df[df['id'] == int(record_id)]
        if row.empty:
            return None
        return row.iloc[0].fillna('').to_dict()

    # ----- Data cleaning helpers -----
    def drop_duplicates(self, subset: Optional[List[str]] = None) -> int:
        """Drop duplicate rows. Returns number of rows removed."""
        df = self._read_df()
        before = len(df)
        df = df.drop_duplicates(subset=subset)
        removed = before - len(df)
        if removed > 0:
            self._write_df(df)
        return int(removed)

    def get_duplicates(self, subset: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        df = self._read_df()
        dup = df[df.duplicated(subset=subset, keep=False)]
        return dup.fillna('').to_dict(orient='records')

    def fill_missing(self, column: str, value: Any) -> int:
        """Fill missing values in a column. Returns number of filled cells."""
        df = self._read_df()
        if column not in df.columns:
            return 0
        mask = df[column].isna()
        count = int(mask.sum())
        if count > 0:
            df.loc[mask, column] = value
            self._write_df(df)
        return count

    def coerce_column_type(self, column: str, dtype: str) -> bool:
        """Attempt to coerce a column to a given dtype (e.g. 'int', 'float', 'datetime').

        Returns True if coercion succeeded (column dtype changed), False otherwise.
        """
        df = self._read_df()
        if column not in df.columns:
            return False
        try:
            if dtype == 'int':
                df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
            elif dtype == 'float':
                df[column] = pd.to_numeric(df[column], errors='coerce')
            elif dtype in ('datetime', 'date'):
                df[column] = pd.to_datetime(df[column], errors='coerce')
            else:
                df[column] = df[column].astype(dtype)
            self._write_df(df)
            return True
        except Exception:
            return False

    def aggregate_sales_by_productline(self) -> Dict[str, List[Any]]:
        """Return labels and values aggregated by PRODUCTLINE for charting."""
        df = self._read_df()
        if 'PRODUCTLINE' not in df.columns or 'SALES' not in df.columns:
            return {'labels': [], 'values': []}
        agg = df.groupby('PRODUCTLINE', dropna=True)['SALES'].sum().sort_values(ascending=False)
        return {'labels': list(agg.index.astype(str)), 'values': list(agg.values.tolist())}

    def sales_over_time(self, date_column: str = 'ORDERDATE', freq: str = 'M') -> Dict[str, List[Any]]:
        """Aggregate sales over time. Expects ORDERDATE parseable by pandas.to_datetime.

        freq examples: 'D' daily, 'M' monthly, 'Y' yearly
        Returns dict with 'labels' (string dates) and 'values'.
        """
        df = self._read_df()
        if date_column not in df.columns or 'SALES' not in df.columns:
            return {'labels': [], 'values': []}
        try:
            dts = pd.to_datetime(df[date_column], dayfirst=True, errors='coerce')
            tmp = df.copy()
            tmp[date_column] = dts
            tmp = tmp.dropna(subset=[date_column])
            series = tmp.set_index(date_column).resample(freq)['SALES'].sum().sort_index()
            labels = [d.strftime('%Y-%m-%d') for d in series.index]
            values = list(series.values.tolist())
            return {'labels': labels, 'values': values}
        except Exception:
            return {'labels': [], 'values': []}
