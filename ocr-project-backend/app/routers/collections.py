''' 
Written by: Simran Bosamiya (sbosami@ncsu.edu)
            Nisarg Shah (nsshah5@ncsu.edu)
'''

from fastapi import Depends, File, UploadFile, APIRouter, HTTPException , status, Response
from typing import List
import os
from app.controller.collections import *
from app.database.connection import *
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas.collection import *

collection_router = APIRouter(prefix="/collections")

@collection_router.get("/get_all/", status_code=status.HTTP_200_OK)
async def get_all_collections_router(response: Response):
    try:
        session = await get_async_session()
        result = await get_collections(session)
        return result
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.get("/get_all_books/", status_code=status.HTTP_200_OK)
async def get_all_books_router(response: Response):
    try:
        session = await get_async_session()
        result = await get_all_books(session)
        return result
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.get("/get_all_periodicals/", status_code=status.HTTP_200_OK)
async def get_all_periodicals_router(response: Response):
    try:
        session = await get_async_session()
        result = await get_all_periodicals(session)
        return result
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.post("/add_book/",  status_code=status.HTTP_201_CREATED)
async def add_book_router(input_data: BookSchema, response: Response):
    try:
        session = await get_async_session()
        result = await add_book(session, input_data)
        # if(result.inserted_primary_key):
        if(result):
            response.status_code = 201
            return "Successfully created collection"
        else:
            response.status_code = 404
            return "Bad request"
    except Exception as e:
        print("EXCEPTION::",e)
        response.status_code = 404
        return "Bad request"

@collection_router.post("/get_books_by_author/",  status_code=status.HTTP_200_OK)
async def get_books_by_auth_router(auth:str,response:Response):
    try:
        session = await get_async_session()
        result = await get_books_by_author(session, auth)
        if(result):
            response.status_code = status.HTTP_200_OK
            return result
        else:
            response.status_code = 201
            return "No matching books found"
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

@collection_router.post("/add_periodical/",  status_code=status.HTTP_201_CREATED)
async def add_periodical_router(input_data: PeriodicalSchema, response: Response):
    try:
        session = await get_async_session()
        result = await add_periodical(session, input_data)
        if(result.inserted_primary_key):
            response.status_code = 201
            return "Successfully created collection"
        else:
            response.status_code = 404
            return "Bad request"
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.post("/collection_by_identifier/",  status_code=status.HTTP_200_OK)
async def get_collection_by_identifier_router(identifier, response: Response):
    try:
        session = await get_async_session()
        result = await get_collection_by_identifier(session, identifier)
        if(result):
            response.status_code = status.HTTP_200_OK
            return result
        else:
            response.status_code = 201
            return "No matching collection found"
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

@collection_router.put("/update_book/",  status_code=status.HTTP_200_OK)
async def update_book_router(input_data: BookSchema, response: Response):
    try:
        session = await get_async_session()
        result = await update_book(session, input_data)
        if(result.rowcount > 0):
            response.status_code = status.HTTP_200_OK
            return "Successfully updated book"
        else:
            response.status_code = 201
            return "No matching book found"
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.put("/update_periodical/",  status_code=status.HTTP_200_OK)
async def update_periodical_router(input_data: PeriodicalSchema, response: Response):
    try:
        session = await get_async_session()
        result = await update_periodical(session, input_data)
        if(result.rowcount > 0):
            response.status_code = status.HTTP_200_OK
            return "Successfully updated periodical"
        else:
            response.status_code = 201
            return "No matching book periodical"
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"

@collection_router.put("/delete_collection/",  status_code=status.HTTP_200_OK)
async def delete_collection_router(identifier: str, response: Response):
    try:
        session = await get_async_session()
        result = await delete_collection(session, identifier)
        if(result.rowcount > 0):
            response.status_code = status.HTTP_200_OK
            return "Successfully deleted collection"
        else:
            response.status_code = 201
            return "No matching collection found"
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"


@collection_router.get("/get_all_authors/", status_code=status.HTTP_200_OK)
async def get_all_authors_router(response:Response):
    try:
        session = await get_async_session()
        result = await get_all_authors(session)
        return result
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"


@collection_router.post("/get_author_by_name/",  status_code=status.HTTP_200_OK)
async def get_auth_by_name_router(auth, response: Response):
    try:
        session = await get_async_session()
        result = await get_author_by_name(session, auth)
        if(result):
            response.status_code = status.HTTP_200_OK
            return result
        else:
            response.status_code = 201
            return "No matching collection found"
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

@collection_router.post("/get_authors_of_book/",  status_code=status.HTTP_200_OK)
async def get_auth_by_book_router(coll_id, response: Response):
    try:
        session = await get_async_session()
        result = await get_authors_of_book(session, coll_id)
        if(result):
            response.status_code = status.HTTP_200_OK
            return result
        else:
            response.status_code = 201
            return "No matching collection found"
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

@collection_router.post("/add_collection/",  status_code=status.HTTP_201_CREATED)
async def add_collection_router(input_data: CollectionSchema, response: Response):
    try:
        session = await get_async_session()
        result = await add_collection(session, input_data)
        if(result.inserted_primary_key):
            response.status_code = 201
            return "Successfully created collection"
        else:
            response.status_code = 404
            return "Bad request"
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"