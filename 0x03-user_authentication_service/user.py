#!/usr/bin/env python3

"""User model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()


class User(Base):
    """This class represent the user table"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    reset_token = Column(String(250), nullable=True)
    session_id = Column(String(250), nullable=True)