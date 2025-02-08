from fetch_links import LinkFetcher
from file_processor import FileProcessor
import time

# from services.data_service import DataService
from io import BytesIO
import requests
from config import BASE_URL
from utils import setup_logger, prepare_data, extract_date_from_url, run_time
from repository.base import SessionLocal
from repository.repository import Repository
from datetime import datetime

logger = setup_logger("app", "logs.log")


target_date = datetime.strptime("31.12.2022", "%d.%m.%Y").date()


@run_time
def run():
    fetcher = LinkFetcher(BASE_URL)

    db = SessionLocal()  # Создаём сессию базы данных
    repository = Repository(db)  # Репозиторий для работы с продуктами
    for file_url in fetcher.fetch_links():
        file_date = extract_date_from_url(file_url)
        if file_date > target_date:
            try:
                start_time = time.time()
                response = requests.get(file_url)
                start_time_1 = time.time()
                el_time = start_time_1-start_time
                logger.info(f"Файл скачан за {el_time} ")
                response.raise_for_status()
                
                
                processor = FileProcessor(BytesIO(response.content))

                processed_data = processor.read_and_process()
                elapsed_time = time.time() - start_time_1
                logger.info(f"Файл оработан за {elapsed_time}")
                if processed_data is not None:
                    for _, row in processed_data.iterrows():
                        product_data = prepare_data(
                            row["exchange_product_id"],
                            row["exchange_product_name"],
                            row["delivery_basis_name"],
                            row["volume"],
                            row["total"],
                            row["count"],
                            file_date,
                        )
                        repository.save_product(product_data)

            except requests.RequestException as e:
                logger.info(f"Ошибка при загрузке файла {file_url}: {e}")
        else:
            record_count = repository.count()
            logger.info(f"Работа закончена, добавлено {record_count} строк")
            break


if __name__ == "__main__":
    run()
