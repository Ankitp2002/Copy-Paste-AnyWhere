from sqlalchemy import create_engine , Column,BIGINT,String,Integer
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


Base =declarative_base()

engin = create_engine("mysql://root:ashu@localhost:3306/fileData")

Session = sessionmaker(bind=engin)

Session = Session()


class FileOpration(Base):
    __tablename__='fileData'

    token=Column(BIGINT,primary_key=True , autoincrement=False)
    fileName = Column(String(220))
    userName = Column(String(220))
    userEmail = Column(EmailType)

class Signup(Base):

    __tablename__ = 'signUp'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(220))
    userEmail = Column(EmailType)
    userPassword = Column(String(220))

class UserFiles(Base):
    __tablename__='userFiles'

    id = Column(Integer, primary_key=True,autoincrement=True)
    fileName = Column(String(220),unique=True)
    userName = Column(String(220))
    userEmail = Column(EmailType)


Base.metadata.create_all(engin)