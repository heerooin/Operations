import pandas as pd
import pytest
from src.report import spending_by_category


def test_spending_by_category():
    test_data = pd.DataFrame([
        {
            'Дата операции': '01.01.2024 12:00:00',
            'Сумма операции': -1000,
            'Категория': 'Продукты'
        },
        {
            'Дата операции': '02.01.2024 12:00:00',
            'Сумма операции': -500,
            'Категория': 'Продукты'
        }
    ])

    result = spending_by_category(test_data, 'Продукты', '15.01.2024')
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Месяц' in result.columns
    assert 'Сумма расходов' in result.columns
    assert 'Количество операций' in result.columns
    assert 'Процент' in result.columns

    assert result['Сумма расходов'].dtype in ['float64', 'int64']
    assert result['Количество операций'].dtype in ['float64', 'int64']
    assert result['Процент'].dtype in ['float64', 'int64']

    assert abs(result['Процент'].sum() - 100) < 0.01

    empty_data = pd.DataFrame(columns=['Дата операции', 'Сумма операции', 'Категория'])
    result = spending_by_category(empty_data, 'Продукты', '15.01.2024')
    assert isinstance(result, pd.DataFrame)
    assert result.empty

    try:
        df = pd.read_excel('../data/operations.xlsx')
        result = spending_by_category(df, 'Продукты', '15.01.2024')
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert 'Месяц' in result.columns
            assert 'Сумма расходов' in result.columns
            assert 'Количество операций' in result.columns
            assert 'Процент' in result.columns
    except FileNotFoundError:
        pass