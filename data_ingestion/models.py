import datetime
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base

engine = db.create_engine("mysql+pymysql://root:root@127.0.0.1:3306/LMS_ORM")
Base = declarative_base()
# meta = db.MetaData()

class Library(Base):
    __table_name__ = "Library"
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    name = db.Column(db.String)
    campus_location = db.Column(db.String)
    email = db.Column(db.String)




