from sqlalchemy import Table, Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    spider = Column(String, nullable=True)
    name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    salary = Column(String, nullable=True)

    def __init__(self, **kwargs):
        self.spider = kwargs.get('spider')
        self.name = kwargs.get('name')
        self.company_name = kwargs.get('company_name')
        self.salary = kwargs.get('salary')
