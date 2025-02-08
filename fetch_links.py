import requests
import httpx
from lxml import html
from utils import setup_logger

logger = setup_logger("LinkFetcher", "logs.log")


class LinkFetcher:
    def __init__(self, base_url):
        self.base_url = base_url

    async def fetch_links(self):
        num_page = 1

        async with httpx.AsyncClient() as client:
            while True:
                url = f"{self.base_url}/markets/oil_products/trades/results/?page=page-{num_page}"
                try:
                    response = await client.get(url)
                    response.raise_for_status()

                    if response.status_code == 200:
                        num_page += 1
                        logger.info(f"Successfully fetched: {url}")
                        tree = html.fromstring(response.content)
                        hrefs = tree.xpath(
                            "//a[contains(@class, 'accordeon-inner__item-title') and "
                            "contains(@class, 'link') and "
                            "contains(@class, 'xls') and "
                            "contains(@href, 'upload')]/@href"
                        )
                        for href in hrefs:
                            logger.info(f"Found file link: {href}")
                            yield f"{self.base_url}{href}"
                    else:
                        logger.warning(
                            f"Failed to fetch {url} with status code: {response.status_code}"
                        )
                        break

                except httpx.RequestError as e:
                    logger.error(f"Error fetching {url}: {e}")
                    break
