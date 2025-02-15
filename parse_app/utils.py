import logging
import time
import re
from datetime import datetime


def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file, mode="w")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def prepare_data(
    exchange_product_id,
    exchange_product_name,
    delivery_basis_name,
    volume,
    total,
    count,
    file_date,
):
    product_data = {
        "exchange_product_id": exchange_product_id,
        "exchange_product_name": exchange_product_name,
        "oil_id": exchange_product_id[:4],
        "delivery_basis_id": exchange_product_id[4:7],
        "delivery_basis_name": delivery_basis_name,
        "delivery_type_id": exchange_product_id[-1],
        "volume": int(volume),
        "total": int(total),
        "count": int(count),
        "date": file_date,
    }
    return product_data


def extract_date_from_url(url):
    try:
        match = re.search(r"\d{14}", url)
        if match:
            date_time = datetime.strptime(match.group(0), "%Y%m%d%H%M%S")
            return date_time.date()
        else:
            print("Дата не найдена в строке.")
            return None
    except ValueError as e:
        print(f"Ошибка при обработке строки даты: {e}")
        return None


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ExecutionTime")


def run_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"Начало выполнения функции {func.__name__}")
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        logger.info(f"Функция {func.__name__} выполнена за {elapsed_time:.2f} секунд")
        return result

    return wrapper
