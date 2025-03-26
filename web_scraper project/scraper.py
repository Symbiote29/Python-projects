import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging
from datetime import datetime
from save_read import save_to_file, read_from_file
from aiohttp_asyncio import fetch_data
from db_con import fetch_data_from_database, save_data_to_database, WebsiteData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()
database_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraped_data.db')
engine = create_engine(f'sqlite:///{database_file}')
Session = sessionmaker(bind=engine)

async def scrape_website(session, url):
    print(f"Scraping data from: {url}")

    async with aiohttp.ClientSession() as session:
        html = await fetch_data(session, url)
        print(f"HTML Length for {url}: {len(html)}")
        soup = BeautifulSoup(html, 'html.parser')

        h2_sections = soup.find_all('h2')
        h3_sections = soup.find_all('h3')
        
        h3_with_h2 = {h3.find_previous('h2') for h3 in h3_sections}

        for i, h2_section in enumerate(h2_sections):
            marker = '*' if h2_section in h3_with_h2 else '-'
            print(f"{i + 1}. {marker} {h2_section.text.strip()}")

        selected_h2_index = input("Select the index of the H2 tag you want to explore: ")

        try:
            selected_h2_index = int(selected_h2_index)
            if 1 <= selected_h2_index <= len(h2_sections):
                selected_h2 = h2_sections[selected_h2_index - 1]
                print(f"\nSelected H2 tag: {selected_h2.text.strip()}\n")
                for i, h3_section in enumerate(h3_sections):
                    if h3_section.find_previous('h2') == selected_h2:
                        print(f"{i + 1}. {h3_section.text.strip()}")

                selected_h3_index = input("Select the index of the H3 tag you want to extract data from: ")
                try:
                    selected_h3_index = int(selected_h3_index)
                    if 1 <= selected_h3_index <= len(h3_sections):
                        selected_h3 = h3_sections[selected_h3_index - 1]
                        data = selected_h3.find_next('p').text.strip()
                        save_to_file(url, data)
                        return data
                    else:
                        print("Invalid H3 tag index.")
                except ValueError:
                    print("Invalid input. Please enter a valid index.")
            else:
                print("Invalid H2 tag index.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

        print(f"No data retrieved for: {url}")
        return None     

async def process_data():
    data_list = await fetch_data_from_database()
    for data in data_list:
        print(f"URL: {data.url}")
        print(f"Data: {data.data}")


async def main():
    urls_input = input("Enter the URLs to scrape (separated by commas): ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    
    if not urls:
        print("No valid URLs provided. Exiting.")
        return

    session = Session()
    
    async with aiohttp.ClientSession() as fetch_session:
        tasks = [scrape_website(fetch_session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        insert_session = Session()
        for url, data in zip(urls, results):
            if data:
                save_data_to_database(url, data)
            else:
                print(f"No data retrieved for: {url}")

        insert_session.commit()
        insert_session.close()
    
    print("Data insertion completed.")
    
    data_list = await fetch_data_from_database()
    print(f"Number of records retrieved: {len(data_list)}")
    
    session.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Starting the scraping process...")
    asyncio.run(main())
    print("Scraping process completed.")
    print("Retrieving and processing data from the database...")
    asyncio.run(process_data())
    print("Data retrieval and processing completed.")
