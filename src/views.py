from src.utils import date_now, cards_info, top_transactions, currency, stocks
import logging
import json
from datetime import datetime


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


def main_view(target_date: datetime = None):
    """
    Отображает главный вид с финансовой информацией.
    """
    logger.info(f"Date in main menu: {target_date}")
    try:
        parsed_data = json.loads(data)
        parsed_data['greeting'] = date_now()
        parsed_data['cards'] = cards_info(target_date)
        parsed_data['top_transactions'] = top_transactions(target_date)
        parsed_data['currency_rates'] = currency()
        parsed_data['stock_prices'] = stocks()
        
        logger.info("Success")
        return parsed_data
    except Exception as e:
        logger.error(f"Error in main menu: {str(e)}")
        raise


if __name__ == '__main__':
    main_view()
