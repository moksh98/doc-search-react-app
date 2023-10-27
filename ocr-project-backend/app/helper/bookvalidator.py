import os
from app.core import settings
from app.helper.validate import UploadValidator
from app.exception.coll_not_found import CollectionNotFoundException, FileTypeException, MissingExtException


class BookValidator(UploadValidator):
    def __init__(self, fn: str, coll_id: str, date: str, volume: str = 0):
        super().__init__(fn)

        self.coll_id = coll_id
        self.date = date
        self.volume = volume

    async def run_checks(self):
        if self.isExtPresent():
            raise MissingExtException(name=self.fn)
        
        if self.isValidType():
            raise FileTypeException(name=self.fn, correct_type=self.VALID_FILETYPES)
        
        if not self.isDateValid():
            raise AttributeError("Incorrect Date format. It should be yyyy or yyyymm or yyyymmdd")

        if not await self.doesCollectionExists():
            raise CollectionNotFoundException(name=self.coll_id)
        
    def isDateValid(self):
        return self.date.isdigit() and len(self.date) in range(4,9)

    def renameFile(self):
        new_name = self.coll_id+"_"+self.date+"_"+self.volume+"."+self.extension
        
        os.rename(
            os.path.join(settings.FILE_STORE, self.fn), 
            os.path.join(settings.FILE_STORE, new_name)
        )