import pytest
from datetime import datetime
from src.utils import date_now, xlsx_open, open_file, cards_info, top_transactions, currency, stocks


def test_date_now():
    greeting = date_now()
    assert isinstance(greeting, str)
    assert greeting in ["Добрый день!", "Добрый вечер!"]


def test_xlsx_open():
    data = xlsx_open('../data/operations.xlsx')
    assert isinstance(data, list)
    
    data = xlsx_open('nonexistent.xlsx')
    assert isinstance(data, list)
    assert len(data) == 0


def test_open_file():
    data = open_file('../data/user_settings.json')
    assert isinstance(data, (dict, list))
    
    data = open_file('nonexistent.json')
    assert isinstance(data, list)
    assert len(data) == 0


def test_cards_info():
    cards = cards_info()
    assert isinstance(cards, list)
    
    test_date = datetime(2024, 1, 1)
    cards = cards_info(test_date)
    assert isinstance(cards, list)


