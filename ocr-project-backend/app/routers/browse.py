''' 
Written by: Mithil Dani (mdani@ncsu.edu)
'''

from fastapi import APIRouter, Response
from app.controller.collections import *
from app.database.connection import *
from app.exception.coll_not_found import CollectionNotFoundException
from app.schemas.collection import *


browse_router = APIRouter(prefix="/browse")


@browse_router.get("/get_collections/")
async def get_collections(coll_type:CollectionTypeEnum, response: Response):
    try:
        session = await get_async_session()
        try:
            stmt = select(Collections.coll_identifier, Collections.coll_name) \
                    .where(Collections.coll_type == coll_type.value) \
                    .order_by(Collections.coll_identifier)
            query_result = await session.execute(stmt)
            response = {}
            for row in query_result:
                response[row[0]] = row[1]
            return response
        finally:
            await close_session(session)
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"


@browse_router.get("/get_periodical_dates/")
async def get_periodical_dates(coll_identifier:str, response: Response):
    try:
        session = await get_async_session()
        
        stmt = select(Periodicals).where(Periodicals.coll_identifier==coll_identifier)
        
        query_result = await session.execute(stmt)
        
        if not query_result:
            raise CollectionNotFoundException(coll_identifier)
        
        result = {}

        for row in query_result:
            periodical = row[0]
            date = periodical.date_of_journal
            
            # add decade
            decade = date.year - (date.year%10)
            decade = f"{decade}-{decade+9}"
            if decade not in result:
                result[decade] = {}

            # add year
            if date.year not in result[decade]:
                result[decade][date.year] = {}

            # add month
            month = date.strftime("%B")
            if month not in result[decade][date.year]:
                result[decade][date.year][month] = {}

            # add date
            result[decade][date.year][month][date] = \
            f"""{periodical.coll_identifier}_""" \
            f"""{str(date.year)}{str(date.strftime('%m'))}{str(date.strftime('%d'))}_""" \
            f"""{periodical.volume}_""" \
            f"""{periodical.issue_number}_""" \
            f"""{periodical.number_of_pages}.pdf"""

        return result

    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"
    finally:
        await close_session(session)

@browse_router.get("/get_book_volumes/")
async def get_book_volumes(coll_identifier:str, response: Response):
    try:
        session = await get_async_session()
        
        stmt = select(Books.coll_identifier, 
                      Books.date_of_publication, 
                      Books.volume,
                      Books.number_of_pages) \
                .where(Books.coll_identifier==coll_identifier)
        
        query = await session.execute(stmt)

        if not query:
            raise CollectionNotFoundException(coll_identifier)
        
        result = {}
        for row in query:
            date = row[1]
            result[row[2]] = \
            f"""{row[0]}_""" \
            f"""{str(date.year)}{str(date.strftime('%m'))}{str(date.strftime('%d'))}_""" \
            f"""{row[2]}_""" \
            f"""{row[3]}.pdf"""

        return result

    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"
    finally:
        await close_session(session)

