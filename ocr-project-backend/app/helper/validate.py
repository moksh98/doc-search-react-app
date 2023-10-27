from app.core.settings import settings
from app.database.connection import get_async_session
from app.controller.collections import get_collection_by_identifier
import filetype
import re
import os
from typing import List

class UploadValidator:

    VALID_FILETYPES = ["pdf"]

    def __init__(self,filename):
        self.fn = filename
        self.extension = None

        self.coll_id = None
        self.date = None
        self.volume = None
        self.coll_info = None

    async def run_checks(self):
        raise NotImplementedError(f"Implement run_checks in {self.__class__.__name__}!!!")

    def isExtPresent(self) -> bool:
        return "." in self.fn

    def isValidType(self) -> bool:
        self.extension=filetype.guess(os.path.join(settings.PDF_IN_STORE,self.fn)).extension
        return self.extension in self.VALID_FILETYPES

    async def doesCollectionExists(self):
        session = await get_async_session()
        result = await get_collection_by_identifier(session,self.coll_id)
        if result:
            self.coll_info = vars(result)
            self.coll_info.pop("_sa_instance_state")
            self.coll_info.pop("new_periodicals")
            self.coll_info.pop("new_books")
            return True
        return False

    def delFile(self):
        os.remove(os.path.join(settings.PDF_IN_STORE,self.fn))