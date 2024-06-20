import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

sql_db_path = os.path.join(pathlib.Path(__file__).parent.parent, "database.db")
sql_db_link = f"sqlite:///{sql_db_path}"

engine = create_engine(sql_db_link, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


