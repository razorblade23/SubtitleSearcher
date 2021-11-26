from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, inspect, exc, MetaData
from sqlalchemy import create_engine, update, delete
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
Base = declarative_base()


engine = create_engine('sqlite:///main.db')
Session = sessionmaker(bind=engine)
session = Session()
inspector = inspect(engine)

class TitloviUsersDB(Base):
    __tablename__ = 'TitloviUsers'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    user_id = Column(String(100))
    token = Column(String(100))
    expiry_datetime = Column(String(100))


    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def set_loggedIn_details(self, user_id, token, expiry_date):
        self.user_id = user_id
        self.token = token
        self.expiry_datetime = expiry_date

class OpenSubtitlesUsersDB(Base):
    __tablename__ = 'OpenSubtitlesUsers'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print('Database built')