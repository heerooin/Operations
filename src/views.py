from src.utils import date_now, cards_info, top_transactions, currency, stocks
import logging
import json


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='finance_reports.log'
)
logger = logging.getLogger(__name__)

data = '''
{
"greeting": "",
  "cards": [
  ],
  "top_transactions": [
  ],
  "currency_rates": [
  ],
  "stock_prices": [
  ]
}
'''


def main():
    parsed_data = json.loads(data)
    parsed_data['greeting'] = date_now()
    parsed_data['cards'] = cards_info()
    parsed_data['top_transactions'] = top_transactions()
    parsed_data['currency_rates'] = currency()
    parsed_data['stock_prices'] = stocks()
    print(parsed_data)


if __name__ == '__main__':
    main()
