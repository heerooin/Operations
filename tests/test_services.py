import pytest
from datetime import datetime
from src.services import cashbacks


def test_cashbacks():
    test_data = [
        {
            'Дата операции': '01.01.2024 12:00:00',
            'Категория': 'Продукты',
            'Бонусы (включая кэшбэк)': 100
        },
        {
            'Дата операции': '02.01.2024 12:00:00',
            'Категория': 'Транспорт',
            'Бонусы (включая кэшбэк)': 50
        }
    ]
    
    result = cashbacks(test_data, 2024, 1)
    assert isinstance(result, dict)
    
    result = cashbacks([], 2024, 1)
    assert isinstance(result, dict)
    assert len(result) == 0
