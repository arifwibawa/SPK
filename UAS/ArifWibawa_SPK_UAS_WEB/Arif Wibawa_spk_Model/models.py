from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mobil(Base):
    __tablename__ = 'mobil'
    id = Column(Integer, primary_key=True)
    nmobil = Column(String(50))
    cc = Column(String(50)) 
    bensin = Column(String(50))
    daya = Column(String(50))
    torsi = Column(String(50))
    harga = Column(String(50))

    def __repr__(self):
        return f"mobil(id={self.id!r}, Nmobil={self.Nmobil!r}"
