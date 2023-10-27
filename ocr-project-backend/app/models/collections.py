''' 
Written by: Simran Bosamiya (sbosami@ncsu.edu)
'''

from sqlalchemy import Column, String, Date, Integer, ForeignKey, PrimaryKeyConstraint, Enum, Sequence, Table, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from citext import CIText

Base: DeclarativeMeta = declarative_base()

class Collections(Base):
    __tablename__ = "new_collections"

    coll_identifier = Column(CIText, primary_key = True)
    coll_name = Column(String, nullable = False)
    coll_location = Column(String, nullable = False)
    # coll_type = Column(Enum("book", "periodical",name="ctype_enum"), nullable = False)
    coll_type = Column(String, nullable = False)
    coll_source = Column(String, nullable = False)

book_author = Table('book_authors', Base.metadata, 
    Column('book_id', CIText),
    Column('author_id', Integer, ForeignKey('new_authors.auth_id')),
    Column('volume', Integer),
    ForeignKeyConstraint(['book_id', 'volume'], ['new_books.coll_identifier', 'new_books.volume'])
)

class Authors(Base):
    __tablename__ = "new_authors"
    auth_id = Column(Integer, primary_key=True)
    author = Column(String, nullable = False, unique=True) 

    books=relationship("Books",secondary=book_author, back_populates="all_authors", lazy="joined")
    
class Books(Base):
    __tablename__ = "new_books"
    date_of_publication = Column(Date, nullable = False)
    number_of_pages = Column(Integer, nullable = False)
    title = Column(String, nullable = False)
    place_of_publication = Column(String, nullable = False)
    publisher = Column(String, nullable = False)
    volume = Column(Integer, nullable = False, primary_key = True)
    language = Column(String, nullable = False)
    coll_identifier = Column(CIText, ForeignKey("new_collections.coll_identifier", ondelete = 'CASCADE'), primary_key = True)
    coll = relationship(Collections, backref=backref("new_books", uselist=True, lazy="subquery", single_parent=True, cascade="all, delete-orphan"))
    # all_authors = relationship(Authors, secondary=book_author, backref=backref('books', lazy="joined"))  

    all_authors=relationship("Authors", secondary=book_author, back_populates="books", lazy="joined")

class Periodicals(Base):
    __tablename__ = "new_periodicals"
    date_of_journal = Column(Date, nullable = False, primary_key = True)
    number_of_pages = Column(Integer, nullable = False)
    volume = Column(Integer, nullable =False, default = 0)
    issue_number = Column(Integer, nullable = False, default = 0)
    coll_identifier = Column(CIText, ForeignKey("new_collections.coll_identifier", ondelete='CASCADE'), primary_key = True)  
    coll = relationship("Collections", backref=backref("new_periodicals", uselist=True, lazy="subquery", single_parent=True, cascade="all, delete-orphan")) 
   
