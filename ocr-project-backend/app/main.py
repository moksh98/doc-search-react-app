from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers.collections import collection_router
from app.routers.uploads import upload as upload_router
from app.routers.search import search as search_router
from app.routers.browse import browse_router
from app.database.connection import *
from app.database.db_session import database_instance

from app.exception.coll_not_found import *

fastapi = FastAPI(title="OCR-Project")

origins = ["*"]

fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# fastapi.add_middleware(ExceptionMiddleware, handlers=fastapi.exception_handlers)

@fastapi.exception_handler(CollectionNotFoundException)
async def collnotfound_exception_handler(request: Request, exc: CollectionNotFoundException):
    return JSONResponse(
        status_code=433,
        content={"message": f" {exc.name} not found in database! Please add information before browsing/uploading..."},
    )

@fastapi.exception_handler(MissingExtException)
async def filetype_exception_handler(request: Request, exc: MissingExtException):
    return JSONResponse(
        status_code=431,
        content={"message": f"uh uh! {exc.name} seems to be missing an extension..."},
    )

@fastapi.exception_handler(FileTypeException)
async def filetype_exception_handler(request: Request, exc: FileTypeException):
    return JSONResponse(
        status_code=432,
        content={"message": f"Oops! {exc.name} is not a PDF file. Please re-upload a proper PDF file..."},
    )

@fastapi.exception_handler(FileNameException)
async def filetype_exception_handler(request: Request, exc: FileNameException):
    return JSONResponse(
        status_code=433,
        content={"message": f" {exc.name} is not a proper fileame. Please check filename before re-uploading..."},
    )


fastapi.include_router(collection_router)
fastapi.include_router(upload_router)
fastapi.include_router(search_router)
fastapi.include_router(browse_router)

@fastapi.get("/")
async def root():
    return {"msg":"HOME PAGE"}

@fastapi.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await database_instance.connect()
    fastapi.state.db = database_instance

@fastapi.on_event("shutdown")
async def shutdown_event():
    if not fastapi.state.db:
        await fastapi.state.db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="info", host="127.0.0.1", port=8001)
