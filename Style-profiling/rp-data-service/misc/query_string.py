import collections
import collections.abc
from django.http import QueryDict

from typing import Mapping, Tuple, List

# constants
_DEFAULT_OFFSET: int = 0
_DEFAULT_LIMIT: int = 20
_MAX_LIMIT: int = 500
_DEFAULT_SORTING_KEY: str = 'sort_by'

# Exceptions
class QueryStringError(Exception):
    '''
    Base exception for query string parsing
    '''
    pass

class QSFilterKeyTypeError(QueryStringError):
    pass

class QSParsingError(QueryStringError):
    pass

class QSParsingFilterError(QSParsingError):
    pass

class QSParsingPaginationError(QSParsingError):
    pass

class QSParsingSortingError(QSParsingError):
    pass


# classes
class QueryStringFilterKeys(dict):
    ''' data structure for filering from query string
        - key: string
        - value: callable for type casting
    '''

    def __init__(self, *args, **kwargs) -> None:
        r = super().__init__(*args, **kwargs)

        for k, v in self.items():
            if not isinstance(k, str):
                raise QSFilterKeyTypeError(f'mapping should be Mapping[str, Callable], but {self}')

            if not callable(v):
                raise QSFilterKeyTypeError(f'mapping should be Mapping[str, Callable], but {self}')

        return r

# functions
def parse_filtering(query_params: QueryDict, filering_keys: QueryStringFilterKeys) -> collections.OrderedDict:

    #
    filering_dict = collections.OrderedDict()

    #
    for key in query_params:
        #
        if key not in filering_keys:
            continue

        #
        values = query_params.getlist(key)
        if len(values) == 0:
            continue

        # type casting
        try:
            _type = filering_keys[key]
            value = _type(values[-1])
        except Exception as excp:
            raise QSParsingFilterError(f'type casting failed: {key}={values[-1]} to {str(_type)}')

        # convert dot notation (e.g. 'a.b.c: v ==> a: {b: {c: v}}')
        if '.' in key:
            splited_keys = key.split('.')

            key = splited_keys[0]
            for splited_key in splited_keys[-1:0:-1]:
                value = {splited_key: value}

        #
        filering_dict[key] = value

    return filering_dict


def parse_pagination(query_params: QueryDict, default_offset: int = _DEFAULT_OFFSET, default_limit: int = _DEFAULT_LIMIT, max_limit:int = _MAX_LIMIT) -> Tuple[int, int]:

    # query_params = query_params.dict()

    #
    offset = query_params.get('offset', default_offset)
    offset = int(offset)
    if offset < 0:
        offset = 0

    #
    limit = query_params.get('limit', default_limit)
    limit = int(limit)
    if limit < 1:
        limit = 1
    if limit > max_limit:
        limit = max_limit

    return offset, limit

def parse_sorting(query_params: QueryDict, sortable_keys: List[str], sorting_key: str = _DEFAULT_SORTING_KEY) -> List[str]:

    #
    sorting_str = ','.join(
        query_params.getlist(sorting_key, [])
    )

    #
    sorting_list = []
    for key in sorting_str.split(','):
        if len(key) == 0:
            continue

        order = '+'
        if key.startswith('+') or key.startswith('-'):
            order = key[0]
            key = key[1:]

        if key not in sortable_keys:
            raise QSParsingSortingError(f'unknown fieldname: {key}')

        # remove '+'
        # see: https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.query.QuerySet.order_by
        if order == '+':
            order = ''

        sorting_list.append(f'{order}{key}')

    return sorting_list

def parse(
    query_params: QueryDict, filering_keys: QueryStringFilterKeys, sortable_keys: List[str], *,
    default_offset:int = _DEFAULT_OFFSET, default_limit:int = _DEFAULT_LIMIT, max_limit:int = _MAX_LIMIT,
    sorting_key:str = _DEFAULT_SORTING_KEY
) -> Tuple[Mapping, int, int, List[str]]:

    filter_map = parse_filtering(query_params, filering_keys)
    offset, limit = parse_pagination(query_params, default_offset, default_limit, max_limit)
    sort_by = parse_sorting(query_params, sortable_keys, sorting_key)

    return filter_map, offset, limit, sort_by