import sys  

from sqlalchemy import Column, ForeignKey, Integer, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship  
from sqlalchemy import create_engine  

Base = declarative_base()  
  
class KFC(Base):
    
    __tablename__ = 'KFC'  
    
    id = Column(Integer, primary_key=True)  
    company = Column(String(250))  
    city = Column(String(250))  
    address = Column(String(250))
    working_hours = Column(String(250))
    phone = Column(String(250))
    
class Burgerking(Base):
    
    __tablename__ = 'Burgerking'  
    
    id = Column(Integer, primary_key=True)  
    company = Column(String(250))  
    city = Column(String(250))  
    address = Column(String(250))
    working_hours = Column(String(250))
    phone = Column(String(250))
    
class Mcdonalds(Base):
    
    __tablename__ = 'Mcdonalds'  
    
    id = Column(Integer, primary_key=True)  
    company = Column(String(250))  
    city = Column(String(250))  
    address = Column(String(250))
    working_hours = Column(String(250))
    phone = Column(String(250))
    
engine = create_engine('sqlite:///K_F_M.db')  
  
Base.metadata.create_all(engine)
