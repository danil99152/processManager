from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from dotenv import load_dotenv
from pathlib import Path
from settings import settings
import os

parent_dir = os.path.dirname(settings.APP_PATH)
dotenv_path = Path(parent_dir + '/.env')
load_dotenv(dotenv_path=dotenv_path)

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
engine = create_engine(SQLALCHEMY_DATABASE_URL)

metadata_obj = MetaData()

app_table = Table(
    "apps",
    metadata_obj,

    Column('pid', Integer, primary_key=True),
    Column('name', String),
    Column('cpu_percent', String),
    Column('memory_percent', String),
    Column('opened_at', DateTime)
)


history_table = Table(
    "history",
    metadata_obj,

    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('pid', Integer),
    Column('name', String),
    Column('opened_at', DateTime),
    Column('closed_at', DateTime)
)