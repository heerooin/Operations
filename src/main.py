from src.views import main_view
from src.services import cashbacks
from src.report import spending_by_category
from src.utils import xlsx_open
import logging
import json
from datetime import datetime


def main():
    """
    Главная функция приложения
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting application")
    
    try:
        operations_data = xlsx_open('../data/operations.xlsx')
        current_date = datetime.now()
        main_view(current_date)
        cashback_data = cashbacks(operations_data, current_date.year, current_date.month)
        logger.info(f"Calculated cashbacks: {cashback_data}")
        spending_report = spending_by_category(
            operations_data,
            category="Продукты",
            date=current_date.strftime("%d.%m.%Y")
        )
        logger.info("Generated spending report")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()
