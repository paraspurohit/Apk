import sqlalchemy
from datetime import datetime
from ebotify.constants.dbConstnat import DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from sqlalchemy import Integer, String, Column, DateTime


Base = declarative_base()


class Events(Base):

    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    sender_id = Column(String, nullable=False)
    data = Column(String)


class Tickets(Base):

    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    createdAt = Column(DateTime, default=datetime.now)
    senderId = Column(String, nullable=False)
    ticketId = Column(String, nullable=False)


class Database():
    
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DB_NAME}')
        self.session = Session(bind=self.engine)

    def createDbTables(self):
        try:
            Base.metadata.create_all(self.engine)
            print("Tables created")
        except Exception as ex:
            print("Error occurred during Table creation!")
            print(ex)

    def addRecord(self, record):
        self.session.add_all(record)
        self.session.new
        self.session.commit()

    def query(self, table):
        return self.session.query(table)

    def deleteRecord(self, table, conditions):
        self.session.query(table).filter(
            conditions).delete(synchronize_session=False)
        self.session.commit()
        return

    def execute(self, statement):
        return self.session.execute(statement)

    def renameTable(self, tableExistingName, tableNewName):
        statement = "ALTER TABLE {} RENAME TO {};".format(
            tableExistingName, tableNewName)
        return self.execute(statement)

    def isTableExist(self, table):
        tables = sqlalchemy.inspect(self.engine).get_table_names()
        if table in tables:
            return True
        return False
