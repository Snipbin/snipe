from typing import List


class SearchUpdate(object):

    def __init__(self, id_, title=None, description=None, code=None, author=None, language=None, last_modified=None,
                 action="upload"):
        self.action = action
        self.id_ = id_
        self.title = title
        self.description = description
        self.code = code
        self.author = author
        self.language = language
        self.last_modified = last_modified


class AzureSearchResponseData(object):

    def __init__(self, id_=None, score=None):
        self.score: float = score
        self.id: str = id_


class AzureSearchResponse(object):
    count: int
    value: List[AzureSearchResponseData]

    def __init__(self, count=0, value=None):
        self.count = count
        self.value = value
