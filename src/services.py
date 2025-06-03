from src.utils import xlsx_open
import pandas as pd
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='finance_reports.log'
)
logger = logging.getLogger(__name__)

info = xlsx_open('../data/operations.xlsx')


def cashbacks(data, year, month) -> dict:
    df = pd.DataFrame(data)
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    filtered = df[
        (df['Дата операции'].dt.year == year) & (df['Дата операции'].dt.month == month)
        ]
    result = (
        filtered.groupby('Категория')['Бонусы (включая кэшбэк)']
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .to_dict()
    )
    return result
