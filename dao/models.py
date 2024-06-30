from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Text, DateTime


Base = declarative_base()


class Email(Base):
    __tablename__ = 'email'
    id = Column(String(20), primary_key=True)
    to_email = Column(String(255), index=True)
    from_email = Column(String(255), index=True)
    subject = Column(Text)
    body = Column(Text)
    received_date = Column(DateTime, index=True)

    @classmethod
    def getattr(cls, column_name: str):
        if cls.__dict__.get(column_name):
            return cls.__dict__.get(column_name)
