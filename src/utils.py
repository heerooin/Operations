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
    """
    Возвращает приветствие в зависимости от времени суток.
    """
    d = datetime.now()
    if int(d.strftime('%H')) <= 17:
        return "Добрый день!"
    else:
        return "Добрый вечер!"


def xlsx_open(file_path):
    """
    Открывает Excel файл и возвращает данные в виде списка словарей.
    """
    try:
        logger.info(f"Opening Excel file: {file_path}")
        df = pd.read_excel(file_path)
        return df.to_dict("records")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []


def open_file(file_path: str) -> list:
    """
    Открывает JSON файл и возвращает его содержимое.
    """
    try:
        logger.info(f"Opening JSON file: {file_path}")
        with open(file_path, encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error opening file {file_path}: {str(e)}")
        return []


def cards_info(target_date: datetime = None):
    """
    Получает информацию о картах и их операциях.
    """
    logger.info(f"Getting cards info for date: {target_date}")
    cards = xlsx_open('../data/operations.xlsx')
    cards_summary = {}
    
    for operation in cards:
        card_number = operation.get('Номер карты')
        if isinstance(card_number, str):
            last_digits = card_number[-4:]
            amount = float(operation.get('Сумма операции', 0))
            cashback = round(amount * 0.01, 2)
            if target_date:
                op_date = pd.to_datetime(operation.get('Дата операции'), format='%d.%m.%Y %H:%M:%S')
                if op_date > target_date:
                    continue
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
    logger.info(f"Found {len(result)} cards")
    return result


def top_transactions(target_date: datetime = None):
    """
    Получает топ-5 транзакций.
    """
    logger.info(f"Getting top transactions for date: {target_date}")
    transactions_data = []
    transactions_summary = {}
    transactions = xlsx_open('../data/operations.xlsx')
    df = pd.DataFrame(transactions)
    if target_date:
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        start_date = target_date.replace(day=1, hour=0, minute=0, second=0)
        df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= target_date)]
    
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
    logger.info(f"Found {len(transactions_data)} top transactions")
    return transactions_data


def currency():
    """
    Получает курсы валют.
    """
    logger.info("Getting currency rates")
    currency_rates = []
    rates = {}
    info = open_file("../data/user_settings.json")
    API_KEY = os.getenv("API_KEY")
    
    if not API_KEY:
        logger.error("API_KEY not found in environment variables")
        return []
    
    url = "https://api.apilayer.com/exchangerates_data/convert"
    for i in info["user_currencies"]:
        try:
            payload = {"amount": "1", "from": i, "to": "RUB"}
            headers = {"apikey": API_KEY}
            response = requests.get(url, headers=headers, params=payload)
            result = response.json()
            rates[i] = {
                'currency': result['query']['from'],
                'rate': round(result['info']['rate'], 2)
            }
            logger.info(f"Got rate for {i}: {rates[i]['rate']}")
        except Exception as e:
            logger.error(f"Error getting rate for {i}: {str(e)}")
    
    currency_rates = list(rates.values())
    return currency_rates


def stocks():
    """
    Получает цены акций.
    """
    logger.info("Getting stock prices")
    current_stocks = []
    stock = {}
    info = open_file("../data/user_settings.json")
    API_STOCKS = os.getenv("API_STOCKS")
    
    if not API_STOCKS:
        logger.error("API_STOCKS not found in environment variables")
        return []
    
    symbols = info["user_stocks"]
    for i in symbols:
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock/full/real-time-price/{i}?apikey={API_STOCKS}"
            response = requests.get(url)
            result = response.json()
            stock[i] = {
                'stock': i,
                'price': result[0]['askPrice']
            }
            logger.info(f"Got price for {i}: {stock[i]['price']}")
        except Exception as e:
            logger.error(f"Error getting price for {i}: {str(e)}")
    
    current_stocks = list(stock.values())
    return current_stocks
