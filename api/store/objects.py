#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,invalid-name,bad-continuation,unused-import,too-few-public-methods
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
eng = create_engine('sqlite:///:memory:')

Base = declarative_base()

class KObj(Base):
    Id = Column(Integer, primary_key=True)
    Version = Column(Integer)
    Encrypted = Column(Boolean)

class Article(KObj):
    Title = Column(String)
    Authors = Column()#one to many
    Sources = Column()#one to many
    Filename = Column(String)
    Url = Column(String)
    Flags = Column()
    Body = Column(String)
    Signature = Column()#one to many

class Author(KObj):
    Title = Column(String)
    Twitter = Column(String)
    Email = Column(String)
    RSA = Column(String)
    ArticleLimit = Column(Integer)

class Sources(KObj):
    Url = Column(String)
    Date = Column(String)
    Opinions = Column()#one to many

class Signature(KObj):
    Reference = Column() #foreign key
    Author = Column() #foreign key
    Proof = Column(String)

class Car(Base):
    __tablename__ = "Cars"

    Id = Column(Integer, primary_key=True)
    Name = Column(String)
    Price = Column(Integer)

Base.metadata.bind = eng
Base.metadata.create_all()

Session = sessionmaker(bind=eng)
ses = Session()

ses.add_all(
   [Car(Id=1, Name='Audi', Price=52642),
    Car(Id=2, Name='Mercedes', Price=57127),
    Car(Id=3, Name='Skoda', Price=9000),
    Car(Id=4, Name='Volvo', Price=29000),
    Car(Id=5, Name='Bentley', Price=350000),
    Car(Id=6, Name='Citroen', Price=21000),
    Car(Id=7, Name='Hummer', Price=41400),
    Car(Id=8, Name='Volkswagen', Price=21600)])
ses.commit()

rs = ses.query(Car).all()

for car in rs:
    print(car.Name, car.Price)
