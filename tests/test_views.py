import pytest
from datetime import datetime
from src.views import main_view


def test_main_view():
    data = main_view()
    assert isinstance(data, dict)
    assert 'greeting' in data
    assert 'cards' in data
    assert 'top_transactions' in data
    assert 'currency_rates' in data
    assert 'stock_prices' in data
    assert isinstance(data['greeting'], str)
    assert isinstance(data['cards'], list)
    assert isinstance(data['top_transactions'], list)
    assert isinstance(data['currency_rates'], list)
    assert isinstance(data['stock_prices'], list)
    test_date = datetime(2024, 1, 1)
    data = main_view(test_date)
    assert isinstance(data, dict)
    assert 'greeting' in data
    assert 'cards' in data
    assert 'top_transactions' in data
    assert 'currency_rates' in data
    assert 'stock_prices' in data
    assert isinstance(data['greeting'], str)
    assert isinstance(data['cards'], list)
    assert isinstance(data['top_transactions'], list)
    assert isinstance(data['currency_rates'], list)
    assert isinstance(data['stock_prices'], list)
