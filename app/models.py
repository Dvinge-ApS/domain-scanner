# app/models.py
import warnings
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

warnings.filterwarnings("ignore", category=DeprecationWarning)
Base = declarative_base()

class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain_name = Column(String(255), nullable=False)
    is_available = Column(Boolean)
    last_checked = Column(DateTime)
    
    __table_args__ = (UniqueConstraint('domain_name', name='uq_domain_name'),)