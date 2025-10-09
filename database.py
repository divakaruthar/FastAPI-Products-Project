from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Password: Test@123
# db_url = "postgresql://fastapi_user:Test@123@localhost:5432/fastapi_products_db"
db_url = "postgresql://fastapi_user:Test%40123@localhost:5432/fastapi_products_db"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind = engine)