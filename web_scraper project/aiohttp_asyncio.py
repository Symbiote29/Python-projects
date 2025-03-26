import asyncio
import aiohttp
from fake_useragent import UserAgent
import logging

logger = logging.getLogger(__name__)

async def fetch_data(session, url, retry_attempts=3, delay=2):
    for attempt in range(retry_attempts):
        try:
            print(f"Fetching data from: {url}")
            async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
                return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Error fetching data from {url}: {e}")
            if attempt < retry_attempts - 1:
                logger.info(f"Retrying... (Attempt {attempt + 2})")
            else:
                logger.warning(f"Max retry attempts reached. Skipping {url}.")
        await asyncio.sleep(delay)
    return None
