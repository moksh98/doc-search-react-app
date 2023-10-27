from typing import List


class CollectionNotFoundException(Exception):
    """raised when Collection is not present/ wrong name is given for the query"""
    def __init__(self, name: str):
        super().__init__(f"{name} Collection is missing!")
        self.name = name
class FileNameException(Exception):
    "Raised when the filename is not according to the specified format!"
    def __init__(self, name: str):
        super().__init__(f"{name} does not follow file naming convention! Please check with Admin!")
        self.name = name
class FileTypeException(Exception):
    "Raised when the file type is incorrect"
    def __init__(self, name: str, correct_type: List[str]):
        super().__init__(f"{name} needs to be from one of the following filetypes: [{', '.join(correct_type)}]!")
        self.name = name
class MissingExtException(Exception):
    "Raised when the file type is absent from filename"
    def __init__(self, name: str):
        super().__init__(f"There's no extension present in file {name}!")
        self.name = name
    
