import os
from fastapi import UploadFile
from app.core.settings import settings
from datetime import datetime

async def save_file_on_server(file:UploadFile):
    try:
        file_path=os.path.join(settings.PDF_IN_STORE,file.filename)
        contents = await file.read()
        size = len(contents)
        with open(file_path, 'wb') as f:
            f.write(contents)
        return file.filename, size
    except Exception:
        raise Exception(f"There was an error uploading the file(s) for {file.filename}")
    finally:
        await file.close()

def get_date(date_of_publish):
    if len(date_of_publish) == 8:
        date_of_publish = datetime.strptime(date_of_publish, '%Y%m%d').date()
    elif len(date_of_publish) == 6:
        # date_of_publish = date_of_publish[:4]+'-'+date_of_publish[4:]+'-01'
        date_of_publish = datetime.strptime(date_of_publish, '%Y%m').date()
    elif len(date_of_publish) == 4:
        date_of_publish = datetime.strptime(date_of_publish, '%Y').date()
    else:
        raise Exception
    return date_of_publish

async def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size