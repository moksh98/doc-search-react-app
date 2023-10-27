from enum import Enum
from pydantic import BaseModel
from datetime import date
from typing import List

class CollectionTypeEnum(Enum):
    periodical = 'periodical'
    book = 'book'


class CollectionSchema(BaseModel):
    coll_identifier: str
    coll_name: str
    coll_location: str
    coll_type: str
    coll_source: str
        

class PeriodicalSchema(CollectionSchema):
    date_of_journal: date
    number_of_pages: int
    coll_identifier: str

class BookSchema(CollectionSchema):
    date_of_publication: date
    number_of_pages: int
    author: str
    title: str
    place_of_publication: str
    publisher: str
    volume: int
    language: str
    coll_identifier: str

class AuthorSchema():
    auth_id:str
    author:str

class BookAuthorSchema():
    coll_identifier:str
    auth_id:str
