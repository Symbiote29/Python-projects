from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()
database_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraped_data.db')
engine = create_engine(f'sqlite:///{database_file}')
Session = sessionmaker(bind=engine)

class WebsiteData(Base):
    __tablename__ = 'website_data'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=False)
    data = Column(String(10000))

async def fetch_data_from_database():
    session = Session()
    query = session.query(WebsiteData)
    data_list = query.all()
    session.close()
    return data_list

def save_data_to_database(url, data):
    session = Session()
    website_data = WebsiteData(url=url, data=data)
    session.add(website_data)
    session.commit()
    session.close()
