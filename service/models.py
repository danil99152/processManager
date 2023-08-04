from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table

engine = create_engine("postgresql://postgres:root@localhost/mt5db")

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