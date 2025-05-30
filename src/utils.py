import json
import os
import requests
from datetime import datetime
import logging
import pandas as pd
from dotenv import load_dotenv


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='finance_reports.log'
)
logger = logging.getLogger(__name__)

load_dotenv()


def date_now() -> str:
    """Функция возвращения даты"""
    d = datetime.now()
    if int(d.strftime('%H')) <= 17:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def xlsx_open(file_path):
    try:
        df = pd.read_excel(file_path)
        return df.to_dict("records")
    except FileNotFoundError:
        return []


def open_file(file_path: str) -> list:
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def cards_info():
    cards = xlsx_open('../data/operations.xlsx')
    cards_summary = {}
    for operation in cards:
        card_number = operation.get('Номер карты')
        if isinstance(card_number, str):
            last_digits = card_number[-4:]
            amount = float(operation.get('Сумма операции', 0))
            cashback = round(amount * 0.01, 2)
            if last_digits in cards_summary:
                cards_summary[last_digits]['total_spent'] += amount
                cards_summary[last_digits]['cashback'] += cashback
            else:
                cards_summary[last_digits] = {
                    'last_digits': last_digits,
                    'total_spent': amount,
                    'cashback': cashback
                }
    result = []
    for card in cards_summary.values():
        result.append({
            'last_digits': card['last_digits'],
            'total_spent': round(card['total_spent'], 2),
            'cashback': round(card['cashback'], 2)
        })
    return result


def top_transactions():
    transactions_data = []
    transactions_summary = {}
    transactions = xlsx_open('../data/operations.xlsx')
    df = pd.DataFrame(transactions)
    sorted_transactions = df.sort_values(by='Сумма платежа').tail()
    for i in reversed(range(5)):
        current = sorted_transactions.iloc[i]
        transactions_summary[i] = {
            'date': current['Дата операции'],
            'amount': float(current['Сумма платежа']),
            'category': current['Категория'],
            'description': current['Описание']
        }
    transactions_data = list(transactions_summary.values())
    return transactions_data


def currency():
    currency_rates = []
    rates = {}
    info = (open_file("../data/user_settings.json"))
    API_KEY = os.getenv("API_KEY")
    url = "https://api.apilayer.com/exchangerates_data/convert"
    for i in info["user_currencies"]:
        payload = {"amount": "1",
                   "from": i,
                   "to": "RUB"}
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers, params=payload)
        result = response.json()
        rates[i] = {'currency': result['query']['from'],
                    'rate': round(result['info']['rate'], 2)}
    currency_rates = list(rates.values())
    return currency_rates


def stocks():
    current_stocks = []
    stock = {}
    info = (open_file("../data/user_settings.json"))
    API_STOCKS = os.getenv("API_STOCKS")
    symbols = info["user_stocks"]
    for i in symbols:
        url = f"https://financialmodelingprep.com/api/v3/stock/full/real-time-price/{i}?apikey={API_STOCKS}"
        response = requests.get(url)
        result = response.json()
        stock[i] = {
            'stock': i,
            'price': result[0]['askPrice']
        }
    current_stocks = list(stock.values())
    return current_stocks


if __name__ == '__main__':
    stocks()
