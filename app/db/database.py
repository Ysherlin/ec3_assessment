from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "mysql+pymysql://root:Test1234@localhost:3306/ec3_leads_db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

Base = declarative_base()
