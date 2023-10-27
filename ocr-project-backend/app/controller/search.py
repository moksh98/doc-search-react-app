''' 
Written by: Simran Bosamiya (sbosami@ncsu.edu)
'''
import asyncio
from typing import List
from app.database.elasticsearchadapter import AsyncElasticSearchAdapter
from app.helper.searchquerybuilder import SearchQueryBuilder
from app.models.collections import *
from app.controller.collections import *
from app.database.connection import *

from app.schemas.search import SearchSchema


async def search_controller(search_data: SearchSchema) -> List[Collections]:

    try:
        if not search_data.search_query or not len(search_data.search_query) > 0:
            raise Exception("Error occured: Invalid search query")

        es_adapter = AsyncElasticSearchAdapter()
        query_builder = SearchQueryBuilder()
        doc = query_builder.build_search_doc(
            search_data.search_query, search_data.match, search_data.sorttype
        )
        print(doc)
        query_task = asyncio.create_task(es_adapter.search(**doc))

        db_session = await get_async_session()
        all_collections = await get_collections(db_session)
        all_collections = [{"coll_location": el.coll_location, "coll_source": el.coll_source,
                            "coll_identifier": el.coll_identifier, "coll_type": el.coll_type, "coll_name": el.coll_name} for el in all_collections]
        final_output = []

        count, docs = await query_task

        for el in docs:
            obj = {}
            temp = el[query_builder.SELECT_FIELD][0].split(".")[0].split("_")
            if (len(temp) != 5):
                print("Invalid filename ", temp)
                continue

            obj['coll_identifier'] = temp[0]
            if ((search_data.from_year > 0 and int(temp[1][:4]) < search_data.from_year) or (search_data.to_year > 0 and int(temp[1][:4]) > search_data.to_year)):
                pass
            elif (len(search_data.coll_identifier) > 0 and temp[0] not in search_data.coll_identifier):
                pass
            else:
                obj['filename'] = el[query_builder.SELECT_FIELD][0]
                coll_obj = [
                    x for x in all_collections if x['coll_identifier'].lower() == temp[0].lower()]
                if coll_obj:
                    obj = {**obj, **coll_obj[0]}
                    obj['date'] = temp[1][:4] + '-' + \
                        temp[1][4:6] + '-' + temp[1][6:]
                    obj['volume'] = int(temp[2])
                    obj['issue'] = int(temp[3])
                    obj['page_number'] = int(temp[4])
                    final_output.append(obj)
        return final_output
    except Exception as e:
        raise Exception("Error occured: ", e)
