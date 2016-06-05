import os
import sys
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Team(Base):
    __tablename__ = 'team'
    id = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    token = Column(String(250), nullable=False)
    bot_token = Column(String(250), nullable=False)
    bot_id = Column(String(250), nullable=False)

class User(Base):
    __tablename__ = 'user'
    id = Column(String(250), primary_key=True)
    #first_name = Column(String(250), nullable=False)
    #last_name = Column(String(250), nullable=False)
    #email = Column(String(250), nullable=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    im_id = Column(String(250))
    team = relationship("Team", foreign_keys=[team_id])
    score = Column(Integer, default=0)
 
class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey('user.id'))
    to_user_id = Column(Integer, ForeignKey('user.id'))
    time_start = Column(DateTime, default=datetime.datetime.utcnow)
    time_end = Column(DateTime, nullable=True)
    #score = Column(Integer, nullable=True)
    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])
 
class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    message = Column(String(250), nullable=False)
    conversation_id = Column(Integer, ForeignKey('conversation.id'))
    conversation = relationship(Conversation)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///db.sqlite')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
