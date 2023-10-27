from fastapi import APIRouter, status, Response
from app.controller.search import *
from app.schemas.search import *
from app.database.connection import *


search = APIRouter()


@search.put("/search/", status_code=status.HTTP_200_OK)
async def search_router(input_data: SearchSchema, response: Response):
    try:
        result = await search_controller(input_data)
        return result
    except Exception as e:
        print(e)
        response.status_code = 404
        return "Bad request"
