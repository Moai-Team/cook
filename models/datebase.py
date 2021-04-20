from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy
from numpy import genfromtxt

DATABASE_NAME = 'application.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

def Load_Data_1(file_name):
    dt_1 = numpy.dtype([('id', 'i'), ('name', 'U30'), ])
    data = genfromtxt(file_name, delimiter=';', skip_header=1, dtype=dt_1)
    return data.tolist()

def Load_Data_2(file_name):
    dt_2 = numpy.dtype([('id', 'i'), ('name', 'U30'), ('img_folder_name', 'U30'), ('calories', 'i'),
                        ('instruction', 'U2000'), ('time_id', 'i'), ('history', 'U1000'), ('advice', 'U1000'), ])
    data2 = genfromtxt(file_name, delimiter=';', skip_header=1, dtype=dt_2)
    return data2.tolist()

def Load_Data_3(file_name):
    dt_3 = numpy.dtype([('id', 'i'), ('minutes', 'i'), ])
    data3 = genfromtxt(file_name, delimiter=';', skip_header=1, dtype=dt_3)
    return data3.tolist()

def create_db():
    Base.metadata.create_all(engine)


