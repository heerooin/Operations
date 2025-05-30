import json
import logging
import pandas as pd
from datetime import datetime
from typing import Optional
from functools import wraps


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='finance_reports.log'
)
logger = logging.getLogger(__name__)


def report_to_file(default_filename: str = "report_{timestamp}.json"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            filename = kwargs.pop('report_filename', None) if 'report_filename' in kwargs else None
            filename = filename or default_filename.format(timestamp=datetime.now().strftime("%Y%m%d_%H%M%S"))
            result = func(*args, **kwargs)
            try:
                if isinstance(result, pd.DataFrame):
                    result.to_json(filename, orient='records', indent=4)
                else:
                    with open(filename, 'w') as f:
                        json.dump(result, f, indent=4)
                logger.info(f"Report saved to {filename}")
            except Exception as e:
                logger.error(f"Failed to save report: {str(e)}")
                raise
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    try:
        required_columns = {'Дата операции', 'Сумма операции', 'Категория'}
        if not required_columns.issubset(transactions.columns):
            missing = required_columns - set(transactions.columns)
            raise ValueError(f"Отсутствуют необходимые колонки: {missing}")
        transactions['Дата операции'] = pd.to_datetime(
            transactions['Дата операции'],
            format='%d.%m.%Y %H:%M:%S',
            errors='coerce'
        )
        transactions = transactions.dropna(subset=['Дата операции'])
        target_date = pd.to_datetime(date, format='%d.%m.%Y') if date else pd.to_datetime(datetime.now())
        start_date = target_date - pd.DateOffset(months=3)
        mask = (
            (transactions['Категория'].str.strip() == category.strip()),
            (transactions['Дата операции'] >= start_date),
            (transactions['Дата операции'] <= target_date),
            (transactions['Сумма операции'] < 0)
        )
        filtered = transactions.loc[mask].copy()
        if filtered.empty:
            return pd.DataFrame(columns=['Месяц', 'Сумма расходов', 'Количество операций', 'Процент'])
        filtered['Месяц'] = filtered['Дата операции'].dt.to_period('M')
        monthly_stats = (
            filtered.groupby('Месяц', as_index=False)
            .agg(
                Сумма_расходов=('Сумма операции', lambda x: abs(x).sum()),
                Количество_операций=('Сумма операции', 'count')
            )
            .sort_values('Месяц')
        )
        monthly_stats = monthly_stats.rename(columns={'Сумма_расходов': 'Сумма расходов'})
        total = monthly_stats['Сумма расходов'].sum()
        monthly_stats['Процент'] = (monthly_stats['Сумма расходов'] / total * 100).round(2)
        monthly_stats['Месяц'] = monthly_stats['Месяц'].dt.strftime('%Y-%m')
        return monthly_stats[['Месяц', 'Сумма расходов', 'Количество операций', 'Процент']]
    except Exception as e:
        logger.error(f"Error in spending_by_category: {str(e)}")
        raise
