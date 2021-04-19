from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy
from numpy import genfromtxt

DATABASE_NAME = 'application.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

def Load_Data(file_name):
    dt_1 = numpy.dtype([('id', 'i'), ('name', 'U30'), ])
    data = genfromtxt(file_name, delimiter=';', skip_header=1, dtype=dt_1)
    return data.tolist()

def create_db():
    Base.metadata.create_all(engine)


