import os
from typing import List
from time import strftime,gmtime
from app.dependencies import get_redis
from fastapi import File, UploadFile, APIRouter, Depends, Form 
from app.core.settings import settings
from app.helper.bookvalidator import BookValidator
from app.helper.periodicalvalidator import PeriodicalValidator
from app.helper.uploadhelper import save_file_on_server, get_size
from app.exception.coll_not_found import * 
from app.tasks.upload import split_pdf_to_images
import fitz
from app.controller.collections import insert_into_periodicals, insert_into_books, delete_into_periodicals
from app.dependencies import get_redis
from app.helper.cachehelper import UsedSpaceCache

cache = get_redis()
upload = APIRouter(prefix="/upload")

@upload.get("/get_storage_cap")
async def get_storage_cap(current_size: int, cache = Depends(get_redis)):
    cache_obj = UsedSpaceCache(cache, key = "used_space")
    used_space = int(cache_obj._get_details())
    if settings.DISK_SPACE < used_space + current_size:
        return {"result": "false"}
    return {"result":"true"}


async def remove_file(filename, filesize, cache_obj):
    os.remove(os.path.join(settings.PDF_IN_STORE, filename))
    cache_obj.delete_file(filesize)

@upload.post("/upload-periodical")
async def upload_periodical(files: List[UploadFile] = File(...), cache = Depends(get_redis)):
    f = open(settings.LOG_FILE, "a")
    f.write("\n==========================================\nStart Upload Periodical: "+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    f.close()
    

    cache_obj = UsedSpaceCache(cache = cache, key = "used_space")
    collection_info = None
    for file in files:
        filename, filesize = await save_file_on_server(file)        
        cache_obj.save_file(filesize)
        # Validate Input data
        try:
            val = PeriodicalValidator(filename)
            await val.run_checks()
        except Exception as e:
            await remove_file(filename, filesize, cache_obj)
            raise e
        
        filename = val.renameFile()
        collection_info = await val.get_data_for_indexing()

        try:
            pdf_reader = fitz.open(os.path.join(settings.PDF_IN_STORE,filename))
            page_count = pdf_reader.page_count
            print("NUMBER OF PAGES::",page_count)
            await insert_into_periodicals(page_count, val)
        except Exception as e:
            await remove_file(filename, filesize, cache_obj)
            raise e
    
        try:
            split_pdf_to_images.delay(filename, collection_info)
            cache_obj.delete_file(filesize)
        except Exception as e:
            await delete_into_periodicals(val)
            await remove_file(filename, filesize, cache_obj)
            raise e

    f = open(settings.LOG_FILE, "a")
    f.write("\nEnd Upload Periodical: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
    f.close()

    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}  


# @upload.post("/upload-book")
# async def upload_book(  date_of_publication: str, 
#                         number_of_pages: str,
#                         author: str,
#                         title: str,
#                         place_of_publication: str,
#                         publisher: str,
#                         volume: str,
#                         language: str,
#                         coll_identifier: str,
#                         file: UploadFile = File(...)):
#     f = open(settings.LOG_FILE, "a")
#     f.write("\n==========================================\nStart Upload Book: "+strftime("%Y-%m-%d %H:%M:%S", gmtime()))
#     f.close()
    

#     filename = await save_file_on_server(file)        

#     # Validate Input data
#     try:
#         val = BookValidator(filename, coll_id=coll_identifier, date = date_of_publication, volume=volume)
#         await val.run_checks()
#     except Exception as e:
#         os.remove(os.path.join(settings.FILE_STORE, filename))
#         raise e
    
#     filename = val.renameFile()
#     # TODO: Save data to PG
#     try:
#         pdf_reader = fitz.open(os.path.join(settings.FILE_STORE,filename))
#         page_count = pdf_reader.page_count
#         # If we are giving the page number then no need to call abvove lines to calculate no. of pages
#         # await insert_into_books(date_of_publication, int(number_of_pages), author, title, place_of_publication, publisher, volume, language, coll_identifier)
#         await insert_into_books(date_of_publication, page_count, author, title, place_of_publication, publisher, volume, language, coll_identifier)
#     except Exception as e:
#         os.remove(os.path.join(settings.FILE_STORE, filename))
#         raise e


#     # TODO: write celery code to perform ocr and adding it to solr
#     # Pdfsplit and processing tasks begin from here
#     split_pdf_to_images(filename)
    
#     f = open(settings.LOG_FILE, "a")
#     f.write("\nEnd Upload Book: "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
#     f.close()

#     return {"message": f"Successfuly uploaded {[file.filename]}"}  

# @upload.get("/getthumbnail", responses={200:{"description":"Returns the thumbnails for the requested filenames"}})
# async def getthumbnail(filename: str):
#     filepath=os.path.join(path,filename)
#     if os.path.exists(filepath):
#         return FileResponse(filepath, media_types="image/jpg")
#     return {"ERROR": "File Not Found!!!"}