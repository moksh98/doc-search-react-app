from enum import Enum
from pydantic import BaseModel
from typing import List


class MatchType(Enum):
    EXACT = "exact"
    ANY = "any"
    ALL = "all"


class SortType(Enum):
    ASC = "asc"
    DESC = "desc"


class SearchSchema(BaseModel):
    search_query: str
    from_year: int
    to_year: int
    coll_identifier: List
    match: MatchType = MatchType.ANY
    sorttype: SortType = SortType.DESC
