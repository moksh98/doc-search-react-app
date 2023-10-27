import os
import re
from typing import List
from app.core.settings import settings
from app.helper.validate import UploadValidator
from app.helper.uploadhelper import get_date
from app.exception.coll_not_found import CollectionNotFoundException, FileNameException, FileTypeException, MissingExtException


class PeriodicalValidator(UploadValidator):
    def __init__(self, fn):
        super().__init__(fn)
        
        self.issue_number = None
        
    async def run_checks(self):
        if not self.isExtPresent():
            raise MissingExtException(name=self.fn)
        
        if not self.isValidType():
            raise FileTypeException(name=self.fn, correct_type=self.VALID_FILETYPES)
        
        if not self.isValidName():
            raise FileNameException(name=self.fn)

        if not await self.doesCollectionExists():
            raise CollectionNotFoundException(name=self.coll_id)
        
    async def get_data_for_indexing(self):
        self.coll_info["volume"] = self.volume
        self.coll_info["issue_number"] = self.issue_number
        self.coll_info["date"] = get_date(self.date)
        return self.coll_info

    def isValidName(self) -> bool:
        
        name_list = self.parse_filename()

        # there should atleast be coll_id and date
        # and at max there should be coll_id, date, vol, issue
        if len(name_list) !=4:
            return False

        if not name_list[0].isalpha() \
           or not name_list[1].isdigit() \
           or not len(name_list[1]) in range(4,9):
            return False
        
        self.coll_id = name_list[0]
        self.date = name_list[1]

        self.volume = int(name_list[2])
        self.issue_number = int(name_list[3])
    
        return True

    def parse_filename(self) -> List[str]:
        # split name based on _
        name_list = self.fn.lower().split(".")[0].split("_")
        return name_list

    def renameFile(self):
        if not self.volume:
            self.volume = 0
        if not self.issue_number:
            self.issue_number = 0
        if len(self.date) == 4:
            self.date += '0101'
        elif len(self.date) == 6:
            self.date += '01'
        
        new_name = self.coll_id+"_"+self.date+"_"+str(self.volume)+"_"+str(self.issue_number)+"."+self.extension
        
        os.rename(
            os.path.join(settings.PDF_IN_STORE, self.fn), 
            os.path.join(settings.PDF_IN_STORE, new_name)
        )
        return new_name

