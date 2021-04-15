from typing import Final, TYPE_CHECKING, Optional, Mapping, Any, Iterable, Tuple, Generator, Dict, Union

from requests import Response

from arago.hiro.abc.common import AbcData
from arago.hiro.abc.search import AbcSearchRest, AbcSearchData

if TYPE_CHECKING:
    from arago.hiro.client.rest_base_client import HiroRestBaseClient


class Hiro7SearchRest(AbcSearchRest):
    __base_client: Final['HiroRestBaseClient']

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        path = client.root.model.meta.version()['graph'].endpoint
        fork = client.fork(path)
        self.__base_client = fork

    def connected(self, vertex_id: str, edge_type: str, params: Optional[Mapping[str, Any]] = None,
                  headers: Optional[Mapping[str, str]] = None, stream: bool = False) -> Response:
        raise NotImplementedError()

    def external_id(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/xid'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def get_by_ids(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/ids'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def index(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/vertices'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )

    def graph(
            self,
            req_data: Mapping[str, Any],
            headers: Optional[Mapping[str, str]] = None,
            stream: bool = False
    ) -> Response:
        uri = '/query/gremlin'
        return self.__base_client.request(
            'POST', uri, headers=headers, json=req_data, stream=stream
        )


class Hiro7SearchData(AbcSearchData):
    __rest_client: Final[Hiro7SearchRest]

    def __init__(self, client: 'HiroRestBaseClient') -> None:
        super().__init__(client)
        self.__rest_client = Hiro7SearchRest(client)

    def connected(
            self,
            vertex_id: str,
            edge_type: str,
            direction: Optional[str] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            vertex_types: Optional[Iterable[str]] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            params: Optional[Mapping[str, str]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        raise NotImplementedError()

    def external_id(
            self,
            external_id: str,
            include_deleted: Optional[bool] = None,  # server default: False
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective request data">
        e_req_data = {
            'query': external_id
        }

        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_req_data['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_req_data['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_data.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        response = self.__rest_client.external_id(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def get_by_ids(
            self,
            *vertex_ids: str,
            include_deleted: Optional[bool] = None,  # server default: False
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective request data">
        e_req_data = {
            'query': ','.join(vertex_ids)
        }

        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_req_data['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if order is not None:
            if isinstance(order, Tuple):
                e_req_data['order'] = ' '.join(order)
            elif isinstance(order, Iterable):
                e_req_data['order'] = ','.join(' '.join(pair) for pair in order)
            else:
                raise TypeError(type(order))

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_req_data['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_data.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        response = self.__rest_client.get_by_ids(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def index(
            self,
            query: str,
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,
            offset: Optional[int] = None,  # server default: 0
            limit: Optional[int] = None,  # server default: 20
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            count: Optional[bool] = None,  # server default: False
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective request data">
        e_req_data = {
            'query': query
        }

        if order is not None:
            if isinstance(order, Tuple):
                e_req_data['order'] = ' '.join(order)
            elif isinstance(order, Iterable):
                e_req_data['order'] = ','.join(' '.join(pair) for pair in order)
            else:
                raise TypeError(type(order))

        if offset is not None:
            if isinstance(offset, int):
                if offset > 0:
                    e_req_data['offset'] = '%i' % offset
                else:
                    raise ValueError('Offset must be an integer greater zero')
            else:
                raise TypeError(type(offset))
        else:
            e_req_data['offset'] = 0

        if limit is not None:
            if isinstance(limit, int):
                if limit > 0:
                    e_req_data['limit'] = '%i' % limit
                else:
                    raise ValueError('Limit must be an integer greater zero')
            else:
                raise TypeError(type(limit))
        else:
            e_req_data['limit'] = -1

        if fields is not None:
            if isinstance(fields, str):
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_req_data['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if count is not None:
            if isinstance(count, bool):
                e_req_data['count'] = str(count).lower()
            else:
                raise TypeError(type(count))

        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_data.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        response = self.__rest_client.index(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items

    def graph(
            self,
            root: str,
            query: str,
            include_deleted: Optional[bool] = None,  # server default: False
            order: Optional[Union[Tuple[str, str], Iterable[Tuple[str, str]]]] = None,  # virtual
            offset: Optional[int] = None,  # virtual
            limit: Optional[int] = None,  # virtual
            fields: Optional[Union[str, Iterable[str]]] = None,
            list_meta: Optional[bool] = None,  # server default: False
            count: Optional[bool] = None,  # virtual
            req_data: Optional[Mapping[str, Any]] = None,
            headers: Optional[Mapping[str, str]] = None
    ) -> Generator[Dict[str, Any], None, None]:
        # <editor-fold name="effective request data">
        e_req_data = {
            'root': root,
            'query': query
        }

        if include_deleted is not None:
            if isinstance(include_deleted, bool):
                e_req_data['includeDeleted'] = str(include_deleted).lower()
            else:
                raise TypeError(type(include_deleted))

        if order is not None:
            # https://tinkerpop.apache.org/docs/3.4.3/reference/#order-step
            stmt = '.order()'
            if isinstance(order, Tuple):
                stmt += f'''.by('{order[0]}', {order[1]})'''
            elif isinstance(order, Iterable):
                stmt += ''.join(f'''.by('{entry[0]}', {entry[1]})''' for entry in order)
            else:
                raise TypeError(type(order))
            e_req_data['query'] += stmt
            del stmt
            # TODO impl hint

        if offset is not None and isinstance(offset, int) and offset < 0:
            raise ValueError('Offset must be an integer greater or equal to zero')
        if limit is not None and isinstance(limit, int) and (limit == 0 or limit < -1):
            raise ValueError('Limit must be an integer greater zero or negative one')
        if offset is not None and limit is None:
            # https://tinkerpop.apache.org/docs/current/reference/#skip-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            stmt = f'.skip({offset})'
            e_req_data['query'] += stmt
            # logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')
            del stmt
        elif offset is None and limit is not None:
            # https://tinkerpop.apache.org/docs/current/reference/#limit-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            stmt = f'.limit({limit})'
            e_req_data['query'] += stmt
            # logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')
            del stmt
        elif offset is not None and limit is not None:
            # https://tinkerpop.apache.org/docs/current/reference/#range-step
            # https://tinkerpop.apache.org/docs/current/reference/#_range_queries deprecated performance reflection
            if limit == -1:
                stmt = f'.skip({offset})'
            else:
                stmt = f'.range({offset},{offset + limit})'
            e_req_data['query'] += stmt
            # logging.debug(f'''appending {stmt!r} to query; resulting query {e_req_data['query']!r}''')
            del stmt

        if fields is not None:
            # ?!? https://tinkerpop.apache.org/docs/3.4.3/reference/#valuemap-step
            if isinstance(fields, str):
                # stmt = f"'{fields}'"
                e_req_data['fields'] = fields
            elif isinstance(fields, Iterable):
                # stmt = ','.join(f"'{field}'" for field in fields)
                e_req_data['fields'] = ','.join(fields)
            else:
                raise TypeError(type(fields))
            # e_req_data['query'] += f'.valueMap({stmt})'
            # del stmt
            # TODO impl hint

        if list_meta is not None:
            if isinstance(list_meta, bool):
                e_req_data['listMeta'] = str(list_meta).lower()
            else:
                raise TypeError(type(list_meta))

        if count is not None:
            if isinstance(count, bool):
                if count is True:
                    # https://tinkerpop.apache.org/docs/current/reference/#count-step
                    e_req_data['query'] += '.count()'
                    # TODO impl hint
                else:
                    pass
            else:
                raise TypeError(type(count))

        if req_data is not None:
            if isinstance(req_data, Mapping):
                e_req_data.update(req_data)
            else:
                raise TypeError(type(req_data))
        # </editor-fold>

        # <editor-fold name="effective headers">
        e_headers = {'Accept': 'application/json'}
        if headers is not None:
            if isinstance(headers, Mapping):
                e_headers.update(headers)
            else:
                raise TypeError(type(headers))
        # </editor-fold>

        response = self.__rest_client.graph(e_req_data, e_headers, stream=True)
        items = AbcData.items_generator(response)
        yield from items
