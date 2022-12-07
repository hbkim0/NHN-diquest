from rest_framework.response import Response
from rest_framework.status import *

from typing import List, Mapping


class ResponseOK(Response):
    def __init__(self, item: Mapping, status: int = HTTP_200_OK):
        super().__init__(data=item, status=status)


class ResponseItem(Response):
    def __init__(self, item: Mapping, status: int = HTTP_200_OK):
        super().__init__(data=item, status=status)


class ResponseItemCreated(Response):
    def __init__(self, item: Mapping, location: str, status: int = HTTP_201_CREATED):
        super().__init__(data=item, status=status, headers={
            'Location': location,
        })


class ResponseItemDeleted(Response):
    def __init__(self, status: int = HTTP_204_NO_CONTENT):
        super().__init__(status=status)


class ResponseNoContent(Response):
    def __init__(self, status: int = HTTP_204_NO_CONTENT):
        super().__init__(status=status)


class ResponseList(Response):
    def __init__(self, total_results: int, results: List[Mapping], *,
                 limit: int = 0, offset: int = 0, sort_by: str = '', filtering: str = '', status: int = HTTP_200_OK):
        super().__init__(data={
            'limit': limit,
            'offset': offset,
            'sort_by': sort_by,
            'filtering': filtering,
            'total_results': total_results,
            'results': results,
        }, status=status)


class ResponseListExtraInfo(Response):
    def __init__(self, total_results: int, results: List[Mapping], info: List[Mapping], *,
                 limit: int = 0, offset: int = 0, sort_by: str = '', filtering: str = '', status: int = HTTP_200_OK):
        super().__init__(data={
            'limit': limit,
            'offset': offset,
            'sort_by': sort_by,
            'filtering': filtering,
            'info': info,
            'total_results': total_results,
            'results': results,
        }, status=status)


class ResponseCount(Response):
    def __init__(self, count: int, filtering: str = '', status: int = HTTP_200_OK):
        super().__init__(data={
            'count': count,
            'filtering': filtering,
        }, status=status)


class ResponseError(Response):
    def __init__(self, error_code: int, error_message: str, status: int):
        super().__init__(data={
            'error_code': error_code,
            'error_message': error_message,
        }, status=status)


class ResponseError400BadRequest(ResponseError):
    def __init__(self, error_code: int, error_message: str):
        super().__init__(error_code, error_message, HTTP_400_BAD_REQUEST)


class ResponseError404NotFound(ResponseError):
    def __init__(self, error_code: int, error_message: str):
        super().__init__(error_code, error_message, HTTP_404_NOT_FOUND)


class ResponseError500InternalServerError(ResponseError):
    def __init__(self, error_code: int, error_message: str):
        super().__init__(error_code, error_message, HTTP_500_INTERNAL_SERVER_ERROR)
