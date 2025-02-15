from parse_app.fetch_links import LinkFetcher
from parse_app.file_processor import FileProcessor
import time
import asyncio
import httpx
from io import BytesIO
import requests
from parse_app.config import BASE_URL
from parse_app.utils import setup_logger, prepare_data, extract_date_from_url, run_time
from repository.base import AsyncSessionLocal, init_db
from repository.repository import Repository
from datetime import datetime

logger = setup_logger("app", "logs.log")

MAX_DOWNLOADS = 10
target_date = datetime.strptime("31.12.2022", "%d.%m.%Y").date()



 
# async def fetch_all_links():
#     fetcher = LinkFetcher(BASE_URL)
#     links = []

#     async for file_url in fetcher.fetch_links():
#         file_date = extract_date_from_url(file_url)
#         if file_date > target_date:
#             links.append(file_url)
#         else:
#             break
    
#     return links

 
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
 
        await init_db()
        fetcher = LinkFetcher(BASE_URL, max_pages=20)
        semaphore = asyncio.Semaphore(MAX_DOWNLOADS)
        tasks = []

        async for file_url in fetcher.fetch_links():
            file_date = extract_date_from_url(file_url)
            if file_date > target_date:
                tasks.append(process_file(file_url, semaphore))
            else:
                break
       
        
        await asyncio.gather(*tasks)
            
        async with AsyncSessionLocal() as db:
            repository = Repository(db)
            record_count = await repository.count()
            logger.info(f"Работа закончена, добавлено {record_count} строк")

 
        
if __name__ == "__main__":
    start_time = time.time()
    #asyncio.run(init_db())
    asyncio.run(run())
    logger.info(f"Время выполнения программы {start_time - time.time():.2f} секунд")