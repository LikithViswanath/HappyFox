from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from utils.env_vars import SQL_ENGINE

Base = declarative_base()


class Email(Base):
    __tablename__ = 'email'
    id = Column(String(20), primary_key=True)
    thread_id = Column(String(20))
    to_email = Column(String(255), index=True)
    from_email = Column(String(255), index=True)
    subject = Column(Text)
    body = Column(Text)
    received_date = Column(DateTime, index=True)


Base.metadata.create_all(SQL_ENGINE)
