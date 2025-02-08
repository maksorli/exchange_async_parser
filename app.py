from fetch_links import LinkFetcher
from file_processor import FileProcessor
import time
import asyncio
import httpx
from io import BytesIO
import requests
from config import BASE_URL
from utils import setup_logger, prepare_data, extract_date_from_url, run_time
from repository.base import AsyncSessionLocal
from repository.repository import Repository
from datetime import datetime

logger = setup_logger("app", "logs.log")

MAX_DOWNLOADS = 10
target_date = datetime.strptime("31.12.2022", "%d.%m.%Y").date()



 
async def fetch_all_links():
    fetcher = LinkFetcher(BASE_URL)
    links = []

    async for file_url in fetcher.fetch_links():
        file_date = extract_date_from_url(file_url)
        if file_date > target_date:
            links.append(file_url)
        else:
            break
    
    return links

 
async def process_file(file_url, semaphore):
     async with semaphore:
        async with AsyncSessionLocal() as db:
            repository = Repository(db)
            try:
                start_time = time.time()
                async with httpx.AsyncClient() as client:
                    response = await client.get(file_url)
                
                start_time_1 = time.time()
                el_time = start_time_1 - start_time
                logger.info(f"Файл {file_url} скачан за {el_time:.2f} секунд")
                response.raise_for_status()

                processor = FileProcessor(BytesIO(response.content))

                # Асинхронная обработка файла в отдельном потоке
                processed_data = await asyncio.to_thread(processor.read_and_process)

                elapsed_time = time.time() - start_time_1
                logger.info(f"Файл {file_url} обработан за {elapsed_time:.2f} секунд")

                if processed_data is not None:
                    product_data_list = [
                        prepare_data(
                            row["exchange_product_id"],
                            row["exchange_product_name"],
                            row["delivery_basis_name"],
                            row["volume"],
                            row["total"],
                            row["count"],
                            extract_date_from_url(file_url),
                        )
                        for _, row in processed_data.iterrows()
                    ]
                    await repository.bulk_save_products(product_data_list)  # Пакетное сохранение

            except httpx.RequestError as e:
                logger.info(f"Ошибка при загрузке файла {file_url}: {e}")


@run_time
async def run():
 

 
        links = await fetch_all_links()
        logger.info(f"Всего найдено {len(links)} ссылок")
        semaphore = asyncio.Semaphore(MAX_DOWNLOADS)
        tasks = [process_file(file_url, semaphore ) for file_url in links]
        await asyncio.gather(*tasks)
            
            
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(run())
    logger.info(f"Время выполнения программы {start_time - time.time():.2f} секунд")