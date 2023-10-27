from copy import deepcopy
import typing as t
from app.schemas.search import MatchType, SortType


class SearchQueryBuilder:

    SEARCH_FIELD = "content"
    SELECT_FIELD = "file_name"

    MATCH_QUERY_BLOCK = {
        "match": {
            f"{SEARCH_FIELD}": None
        }
    }

    MATCH_PHRASE_QUERY_BLOCK = {
        "match_phrase": {
            f"{SEARCH_FIELD}": None
        }
    }

    BOOL_QUERY_BLOCK = {
        "bool": {
            "should": [],
            "must_not": [],
            "must": []
        }
    }

    def _get_any_query_block(self, search_term: str):
        """
        Match Any word
        Doc must contain either new or york or both anywhere in the doc
        {
            "match": {
                "text": "new york"
            }
        }
        """
        any_query_block = deepcopy(self.MATCH_QUERY_BLOCK)
        any_query_block["match"][self.SEARCH_FIELD] = search_term
        return any_query_block

    def _get_all_query_block(self, search_term: str):
        """
        Match all words
        Doc must contain both new and york anywhere in the doc
        {
            "bool": {
                "must": [
                    {
                        "match": {
                            "text": "new"
                        }
                    },
                    {
                        "match": {
                            "text": "york"
                        }
                    }
                ]
            }
        }
        """
        all_query_block = deepcopy(self.BOOL_QUERY_BLOCK)
        terms = search_term.split(" ")
        must_terms_list = []
        for term in terms:
            match_query_block = deepcopy(self.MATCH_QUERY_BLOCK)
            match_query_block["match"][self.SEARCH_FIELD] = term
            must_terms_list.append(match_query_block)
        all_query_block["bool"]["must"] = must_terms_list
        return all_query_block

    def _get_exact_query_block(self, search_term: str):
        """
        Doc Must contain exact word together in the doc
        {
            "match_phrase": {
               "text": "new york"
            }
        }
        """
        exact_query_block = deepcopy(self.MATCH_PHRASE_QUERY_BLOCK)
        exact_query_block["match_phrase"][self.SEARCH_FIELD] = search_term
        return exact_query_block

    def _get_query(self, search_term, match_type):
        if match_type == MatchType.ANY:
            return self._get_any_query_block(search_term)
        elif match_type == MatchType.ALL:
            return self._get_all_query_block(search_term)
        elif match_type == MatchType.EXACT:
            return self._get_exact_query_block(search_term)
        else:
            raise NotImplementedError(
                f"Query builder not available for match type {match_type}")

    def _get_sort(self, sort_type):
        return [
            {
                "_score": {
                    "order": sort_type.value
                }
            }
        ]

    def _get_fields(self):
        return [self.SELECT_FIELD]

    def build_search_doc(self, search_term: str, match_type: MatchType = MatchType.ANY, sort_type: SortType = SortType.DESC) -> t.Mapping[str, t.Any]:
        return {
            "query": self._get_query(search_term, match_type),
            "fields": self._get_fields(),
            "sort": self._get_sort(sort_type),
        }
