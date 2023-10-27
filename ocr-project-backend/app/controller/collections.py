

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm import selectinload
from typing import List
from app.models.collections import *
from app.schemas.collection import *
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from app.database.connection import get_async_session
# from datetime import datetime
from app.helper.uploadhelper import get_date

async def get_collection_by_identifier(session: Session, identifier) -> Collections:
    try:
        stmt = select(Collections).where(Collections.coll_identifier == identifier)
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def get_collections(session) -> List[Collections]:
    try:
        stmt = select(Collections)
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def get_all_books(session) -> List[Collections]:
    try:
        stmt = select(Collections).where(Collections.coll_type == 'book')
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def get_all_periodicals(session) -> List[Collections]:
    try:
        stmt = select(Collections).where(Collections.coll_type == 'periodical')
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def add_collection(session, collection_obj) -> Collections:
    try:
        stmt = insert(Collections).values(coll_identifier=collection_obj.coll_identifier, coll_name=collection_obj.coll_name, coll_location=collection_obj.coll_location, coll_type=collection_obj.coll_type, coll_source=collection_obj.coll_source)
        result = await session.execute(stmt)
        return result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def update_collection(session, collection_obj) -> Collections:
    try:
        stmt = update(Collections).values(coll_name=collection_obj.coll_name, coll_location=collection_obj.coll_location, coll_type=collection_obj.coll_type, coll_source=collection_obj.coll_source).where(Collections.coll_identifier == collection_obj.coll_identifier)
        result = await session.execute(stmt)
        return result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def delete_collection(session: Session, identifier) -> Collections:
    try:
        stmt = delete(Collections).where(Collections.coll_identifier == identifier)
        result = await session.execute(stmt)
        return result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def add_periodical(session, periodical_obj) -> Periodicals:
    try:
        coll_result = await add_collection(session, periodical_obj)
        if(coll_result.inserted_primary_key):
            stmt = insert(Periodicals).values(coll_identifier=periodical_obj.coll_identifier, date_of_journal=periodical_obj.date_of_journal, number_of_pages=periodical_obj.number_of_pages)
            periodical_result = await session.execute(stmt)
            return periodical_result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

    

async def update_book(session, book_obj) -> Books:
    try:
        coll_result = await update_collection(session, book_obj)
        if(coll_result.rowcount > 0):
            book_obj=book_obj.new_books
            stmt = update(Books).values(date_of_publication=book_obj.date_of_publication, number_of_pages=book_obj.number_of_pages,  author=book_obj.author, title=book_obj.title, place_of_publication=book_obj.place_of_publication, publisher=book_obj.publisher, volume=book_obj.volume, language=book_obj.language).where(Books.coll_identifier == book_obj.coll_identifier)
            book_result = await session.execute(stmt)
            return book_result
        else:
            raise Exception("Error occured in inserting collection: ", e)
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

# async def add_periodical(session, periodical_obj) -> Periodicals:
#     try:
#         coll_result = await add_collection(session, periodical_obj)
#         if(coll_result.inserted_primary_key):
#             stmt = insert(Periodicals).values(coll_identifier=periodical_obj.coll_identifier, date_of_journal=periodical_obj.date_of_journal, number_of_pages=periodical_obj.number_of_pages)
#             periodical_result = await session.execute(stmt)
#             return periodical_result
#     except Exception as e:
#         raise Exception("Error occured: ", e)
#     finally:
#         await close_session(session)


async def update_periodical(session, periodical_obj) -> Periodicals:
    try:
        coll_result = await update_collection(session, periodical_obj)
        if(coll_result.rowcount > 0):
            periodical_obj=periodical_obj.new_periodicals
            stmt = update(Periodicals).values(date_of_journal=periodical_obj.date_of_journal, number_of_pages=periodical_obj.number_of_pages).where(Periodicals.coll_identifier == periodical_obj.coll_identifier)
            periodical_result = await session.execute(stmt)
            return periodical_result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def get_all_authors(session) -> List[Authors]:
    try:
        print("here")
        stmt = select(Authors)
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)


async def get_author_by_name(session,auth) -> List[Authors]:
    try:
        stmt = select(Authors).where(func.lower(Authors.author).like(func.lower(auth)))
        result = await session.execute(stmt)
        return result.scalars().first()
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def add_author(session,author) -> Authors:
    try:
        stmt=insert(Authors).values(author=author)
        result = await session.execute(stmt)
        print("Author Inserted")
        return result
    except Exception as e:
        raise Exception("Error occured ", e)
    finally:
        await close_session(session)

async def add_book(session, book_obj) -> Books:
    try:
        coll_result = await add_collection(session, book_obj)
        if(coll_result.inserted_primary_key):
            book=Books(coll_identifier=book_obj.coll_identifier, date_of_publication=book_obj.date_of_publication, number_of_pages=book_obj.number_of_pages, title=book_obj.title, place_of_publication=book_obj.place_of_publication, publisher=book_obj.publisher, volume=book_obj.volume, language=book_obj.language)
            authors=book_obj.author.split(",")
            for author in authors:
                author=author.strip()
                temp_res= await get_author_by_name(session,author)
                if temp_res is None:
                    temp_res = Authors(author=author)
                    session.add(temp_res)
                
                print("AUTHOR::",temp_res.author)

                book.all_authors.append(temp_res)

            session.add(book)
            print("Book added")
            return True
        else:
            raise Exception("Error occured in inserting collection: ", e)
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def get_books_by_author(session, auth) -> List[Collections]:
    try:
        temp_res= await get_author_by_name(session,auth)
        if temp_res is not None:
            author_book = temp_res.books
            return author_book
        else:
            return temp_res
    except Exception as e:
        raise Exception("Error Occured:",e)
    finally:
        await close_session(session)


async def get_authors_of_book(session, book) -> List[Authors]:
    try:
        stmt= select(Books).where(Books.coll_identifier==book)
        author = await session.execute(stmt)
        authors=author.scalars().first()
        return authors.all_authors
    except Exception as e:
        raise Exception("Error Occured:",e)
    finally:
        await close_session(session)

async def insert_into_periodicals(page_count, val):
    session = await get_async_session()
    try:
        stmt = insert(Periodicals).values(date_of_journal=get_date(val.date), number_of_pages=page_count, coll_identifier=val.coll_id, volume=val.volume, issue_number=val.issue_number)
        result = await session.execute(stmt)
        return result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def delete_into_periodicals(val):
    session = await get_async_session()
    try:
        stmt = delete(Periodicals).where(Periodicals.coll_identifier == val.coll_id and Periodicals.date_of_journal == get_date(val.date))
        result = await session.execute(stmt)
        return result
    except Exception as e:
        raise Exception("Error occured: ", e)
    finally:
        await close_session(session)

async def insert_into_books(date_of_publication, page_count, author, title, place_of_publication, publisher, volume, language, coll_identifier):
    session = await get_async_session()
    try:
        stmt = insert(Books).values(date_of_publication=date_of_publication, number_of_pages=page_count, author=author, title=title, place_of_publication=place_of_publication, publisher=publisher, volume=volume, language=language, coll_identifier=coll_identifier)
        result = await session.execute(stmt)
        return result
    except Exception as e:
            raise Exception("Error occured: ", e)
    finally:
            await close_session(session)

async def close_session(session):
    await session.commit()
    await session.close()

