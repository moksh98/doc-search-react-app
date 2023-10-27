from app.database.connection import get_async_session
from app.controller.collections import *

def get_date(date_of_publish):
    if len(date_of_publish) == 8:
        date_of_publish = date_of_publish[:4]+'-'+date_of_publish[4:6]+'-'+date_of_publish[6:]
    elif len(date_of_publish) == 6:
        date_of_publish = date_of_publish[:4]+'-'+date_of_publish[4:]+'-01'
    else:
        date_of_publish = splitname[1]+'-01-01'

    return date_of_publish

async def saveFile(filename):
    name_lst=filename.split("_")
    if len(name_lst) == 2:
        page_no=name_lst[1]

        splitname =  re.split(r'(\d+)',name_lst[0])
        coll_identifier = splitname[0]
        date = splitname[1]
    elif len(name_lst) == 3:
        coll_identifier,date,page_no = name_lst[0], name_lst[1], name_lst[2]
    elif len(name_lst) == 4:
        coll_identifier = name_lst[0]
        if name_lst[1].isdigit():
            date = name_lst[1]
            issue = name_lst[2]
            page_no = name_lst[3]
        else:
            date = name_lst[2]
            page_no = name_lst[3]
    else:
        coll_identifier,date,issue,page_no = name_lst[0],name_lst[2],name_lst[3],name_lst[4]

    date_of_publish=get_date(date)
    if issue is not None:
        issue=issue.lstrip("0") 
    page_no=page_no.lstrip("0")
    
    session = await get_async_session()
    result = await get_collection_by_identifier(session, coll_identifier)

    if(result):
        flag=0
        #update page number based on books or periodicals
        if(result.coll_type=="book"):
            try:
                result.new_books.number_of_pages+=1
                ubook=await update_book(session,result)
            except Exception as e:
                raise Exception("Book not updated. Error occured",e)
            finally:
                await close_session(session)

        elif(result.coll_type=="periodical"):
            try:
                result.new_periodicals.number_of_pages+=1
                uperiodical=await update_periodical(session,period_detail)
            except Exception as e:
                raise Exception("Periodical not updated. Error occured",e)
            finally:
                await close_session(session)
        else:
            raise Exception("No book/Periodical found!")
    else:
        raise Exception("Collection identifier not found!! PLease add it first and then upload files")
    await close_session(session)
