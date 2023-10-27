from uploadhelper import get_size
from app.core.settings import settings

class UsedSpaceCache():
    cache = None
    key: str = ""
    TIMEOUT = 60 * 60 * 2   # 2 hours

    def __init__(self, cache, key:str):
        self.cache = cache
        self.key = key

    def _get_details(self):
        current_space = self.cache.get(self.key)

        if not current_space:
            current_space = await get_size(start_path = settings.PDF_IN_STORE)
            self.save_details(current_space)

        return int(current_space)

    def _save_details(self, used_space):
        self.cache.set(self.key, current_space, timeout = TIMEOUT)

    def save_file(self, filesize):
        current_space = self._get_details()
        self._save_details(current_space + filesize)

    def delete_file(self, filesize):
        current_space = self._get_details()
        self._save_details(current_space - filesize)
