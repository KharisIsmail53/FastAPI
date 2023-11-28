from config.db import meta
from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import INTEGER, VARCHAR, Column

Base = declarative_base()

# class Students(Base):
#     __tablename__ = 'students'
#     id = Column('id', INTEGER, primary_key=True)
#     name = Column('name', VARCHAR(255), nullable=False)
#     age = Column('age', INTEGER, nullable=False)
#     country = Column('country', VARCHAR(255), nullable=False)



students=Table(
    'students',meta,
    Column('id',Integer,primary_key=True),
    Column('name',String(255)),
    Column('age',Integer),
    Column('country',String(255)),
)

