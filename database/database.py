# %% Install packages
# !pip install --upgrade pip
# !pip install sqlalchemy
# !pip install psycopg2-binary
# !pip install pickleshare


# %% Import packages
from database.model import Base

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker 

# Import the config file
from config import DATABASE_URL

# %% Connect to the database
try:
    print(DATABASE_URL)
    # Step 1: Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    # Step 2: Create a session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Step 3: Create a session
    session = SessionLocal()
    # Step 4: Execute a test query
    result = session.execute(text("SELECT version();"))
    for row in result:
        print(f"Connected to - {row[0]}")
except Exception as error:
    print(f"Error connecting to PostgreSQL: {error}")
    

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()

# %%
