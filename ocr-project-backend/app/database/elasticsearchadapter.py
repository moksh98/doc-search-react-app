import typing as t
from elasticsearch import AsyncElasticsearch, Elasticsearch, NotFoundError
from app.core.settings import settings


class BaseElasticSearchAdapter:
    search_index = settings.ES_SEARCH_INDEX
    timeout: float = 3.0

    def __init__(self, is_async: bool = False) -> None:
        self.is_async = is_async
        self.es_client = self.get_client()

    def get_client(self):
        klass = AsyncElasticsearch if self.is_async else Elasticsearch
        return klass(
            settings.ES_HOST,
            basic_auth=(settings.ES_USER, settings.ES_PASS)
        )


class SyncElasticSearchAdapter(BaseElasticSearchAdapter):

    def __init__(self) -> None:
        super().__init__(is_async=False)

    def index(self, document: t.Mapping[str, t.Any], **kwargs):
        """
        Index document into particular index in ES
        """
        return self.es_client.index(index=self.search_index, document=document, **kwargs)

    def get(self, id: str, **kwargs):
        """
        Gets document from the index by id
        :param id: ID of the document
        :param kwargs:
        :return: _source if document found, None otherwise
        """
        try:
            response = self.es_client.get(
                index=self.search_index, id=id, **kwargs)
            return response["_source"]
        except NotFoundError:
            pass
        return None

    def search(self, **kwargs):
        """
        searches
        :param kwargs: same as Elasticsearch.search
        :return:
        """
        response = self.es_client.search(**kwargs)
        count = response["hits"]["total"]["value"]
        if response["hits"]["hits"] and response["hits"]["hits"][0].get("fields"):
            fields = [r["fields"] for r in response["hits"]["hits"]]
            return count, fields
        if response["hits"]["hits"] and response["hits"]["hits"][0]["_source"]:
            source = [r["_source"] for r in response["hits"]["hits"]]
            return count, source
        return count, None

    def update(self, id: str, doc: t.Mapping[str, t.Any], **kwargs):
        """
        :param index:
        :param id:
        :param doc:
        :param kwargs:
        :return:
        """
        return self.es_client.update(index=self.search_index, id=id, doc=doc, **kwargs)

    def delete(self, id: str, **kwargs):
        """
        Delete document of ID from index
        :param id: ID of document to delete
        :param kwargs:
        :return: None
        """
        try:
            return self.es_client.delete(index=self.search_index, id=id, **kwargs)
        except NotFoundError:
            return None

    def count(self, **kwargs):
        """
        gives count of resultant query
        :param kwargs: same as Elasticsearch.count
        :return: Count response
        """
        response = self.es_client.count(**kwargs)
        return response

    def delete_by_query(self, **kwargs):
        """
        delete all documents as per query
        :param kwargs: same as ES client.delete_by_query
        """
        return self.es_client.delete_by_query(**kwargs)


class AsyncElasticSearchAdapter(BaseElasticSearchAdapter):

    def __init__(self) -> None:
        super().__init__(is_async=True)

    async def index(self, document: t.Mapping[str, t.Any], **kwargs):
        """
        Index document into particular index in ES
        """
        return await self.es_client.index(index=self.search_index, document=document, **kwargs)

    async def get(self, id: str, **kwargs):
        """
        Gets document from the index by id
        :param id: ID of the document
        :param kwargs:
        :return: _source if document found, None otherwise
        """
        try:
            response = await self.es_client.get(index=self.search_index, id=id, **kwargs)
            return response["_source"]
        except NotFoundError:
            pass
        return None

    async def search(self, **kwargs):
        """
        searches
        :param kwargs: same as Elasticsearch.search
        :return:
        """
        response = await self.es_client.search(**kwargs)
        count = response["hits"]["total"]["value"]
        if response["hits"]["hits"] and response["hits"]["hits"][0].get("fields"):
            fields = [r["fields"] for r in response["hits"]["hits"]]
            return count, fields
        if response["hits"]["hits"] and response["hits"]["hits"][0]["_source"]:
            source = [r["_source"] for r in response["hits"]["hits"]]
            return count, source
        return count, []

    async def update(self, id: str, doc: t.Mapping[str, t.Any], **kwargs):
        """
        :param index:
        :param id:
        :param doc:
        :param kwargs:
        :return:
        """
        return await self.es_client.update(index=self.search_index, id=id, doc=doc, **kwargs)

    async def delete(self, id: str, **kwargs):
        """
        Delete document of ID from index
        :param id: ID of document to delete
        :param kwargs:
        :return: None
        """
        try:
            return await self.es_client.delete(index=self.search_index, id=id, **kwargs)
        except NotFoundError:
            return None

    async def count(self, **kwargs):
        """
        gives count of resultant query
        :param kwargs: same as Elasticsearch.count
        :return: Count response
        """
        response = await self.es_client.count(**kwargs)
        return response

    async def delete_by_query(self, **kwargs):
        """
        delete all documents as per query
        :param kwargs: same as ES client.delete_by_query
        """
        return await self.es_client.delete_by_query(**kwargs)
