from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50))
    source = Column(String(100))
    created_time = Column(DateTime, nullable=False)
