import asyncio
import httpx
from lxml import html
from utils import setup_logger

logger = setup_logger("LinkFetcher", "logs.log")


class LinkFetcher:
    def __init__(self, base_url, max_pages=10):
        self.base_url = base_url
        self.max_pages = max_pages




    async def fetch_page(self, client, page_num):
  
        url = f"{self.base_url}/markets/oil_products/trades/results/?page=page-{page_num}"
        try:
            response = await client.get(url)
            response.raise_for_status()

            if response.status_code == 200:
                logger.info(f"Successfully fetched: {url}")
                tree = html.fromstring(response.content)
                hrefs = tree.xpath(
                    "//a[contains(@class, 'accordeon-inner__item-title') and "
                    "contains(@class, 'link') and "
                    "contains(@class, 'xls') and "
                    "contains(@href, 'upload')]/@href"
                )
                return [f"{self.base_url}{href}" for href in hrefs]
        except httpx.RequestError as e:
            logger.error(f"Error fetching {url}: {e}")
        return []   

    async def fetch_links(self):
   
        num_page = 1

        async with httpx.AsyncClient() as client:
            while True:
              
                tasks = [self.fetch_page(client, num_page + i) for i in range(self.max_pages)]
                results = await asyncio.gather(*tasks)

               
                all_links = [link for sublist in results for link in sublist]
                
                if not all_links:  
                    break

                for link in all_links:
                    logger.info(f"Found file link: {link}")
                    yield link

                num_page += self.max_pages   
 