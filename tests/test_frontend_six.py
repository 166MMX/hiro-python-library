import json
from datetime import date, datetime, time, timezone
from typing import Generator, ContextManager
from uuid import uuid4

# noinspection PyPackageRequirements
import pytest
from requests import Response

from arago.hiro.client.client import HiroClient
from arago.hiro.model.auth import SessionCredentials, AccessToken
from arago.hiro.model.graph.edge import Edge
from arago.hiro.model.graph.vertex import VertexId, Vertex
from arago.hiro.model.storage import BlobVertex, TimeSeriesValue, TimeSeriesVertex
from arago.hiro.utils.datetime import datetime_to_timestamp_ms
from arago.ogit import OgitEntity, OgitVerb


def uuid() -> str:
    return str(uuid4())


class TestClassMetaInfo:
    def test_info_rest(self, client: HiroClient):
        meta = client.rest.meta
        res = meta.info()
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_info_data(self, client: HiroClient):
        meta = client.data.meta
        res = meta.info()
        assert isinstance(res, dict)

    def test_info_model(self, client: HiroClient):
        meta = client.model.meta
        res = meta.info()
        assert isinstance(res, dict)

    def test_version_rest(self, client: HiroClient):
        meta = client.rest.meta
        with pytest.raises(NotImplementedError):
            res = meta.version()
            res.raise_for_status()
            assert isinstance(res, Response)

    def test_version_data(self, client: HiroClient):
        meta = client.data.meta
        res = meta.version()
        assert isinstance(res, dict)

    def test_version_model(self, client: HiroClient):
        meta = client.model.meta
        res = meta.version()
        assert isinstance(res, dict)

    def test_versions_rest(self, client: HiroClient):
        meta = client.rest.meta
        with pytest.raises(NotImplementedError):
            res = meta.versions()
            res.raise_for_status()
            assert isinstance(res, Response)

    def test_versions_data(self, client: HiroClient):
        meta = client.data.meta
        res = meta.versions()
        assert isinstance(res, dict)

    def test_versions_model(self, client: HiroClient):
        meta = client.model.meta
        res = meta.versions()
        assert isinstance(res, dict)


class TestClassHealth:
    def test_health_rest(self, client: HiroClient):
        health = client.rest.health
        res = health.check()
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_health_data(self, client: HiroClient):
        health = client.data.health
        res = health.check()
        assert isinstance(res, dict)

    def test_health_model(self, client: HiroClient):
        health = client.model.health
        res = health.check()
        assert isinstance(res, dict)


# noinspection PyUnusedLocal
class TestClassAuth:
    def test_token_get_rest(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.rest.auth
        req_data = {
            'client_id': credentials.client.id,
            'client_secret': credentials.client.secret,
            'username': credentials.account.username,
            'password': credentials.account.password,
        }
        res = auth.password(req_data)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_token_get_data(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.data.auth
        res = auth.password(
            credentials.client.id,
            credentials.client.secret,
            credentials.account.username,
            credentials.account.password,
        )
        assert isinstance(res, dict)

    def test_token_get_model(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.model.auth
        res = auth.password(credentials)
        assert isinstance(res, AccessToken)

    @pytest.mark.skip
    def test_token_refresh_rest(self, client: HiroClient):
        auth = client.rest.auth

    @pytest.mark.skip
    def test_token_refresh_data(self, client: HiroClient):
        auth = client.data.auth

    @pytest.mark.skip
    def test_token_refresh_model(self, client: HiroClient):
        auth = client.model.auth

    def test_token_revoke_rest(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.rest.auth
        req_data = {
            'client_id': credentials.client.id,
        }
        res = auth.revoke(req_data)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_token_revoke_data(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.data.auth
        auth.revoke(credentials.client.id)

    def test_token_revoke_model(self, client: HiroClient, credentials: SessionCredentials):
        auth = client.model.auth
        auth.revoke(credentials.client)


class TestClassGraph:
    def test_vertex_create_rest(self, client: HiroClient):
        graph = client.rest.graph
        vertex_type = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.create(vertex_type, {})
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_vertex_create_data(self, client: HiroClient):
        graph = client.data.graph
        vertex_type = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.create(vertex_type)
        assert isinstance(res, dict)

    def test_vertex_create_model(self, client: HiroClient):
        graph = client.model.graph
        vertex_type = OgitEntity.OGIT_COMMENT
        res = graph.vertex.create(vertex_type)
        assert isinstance(res, Vertex)

    def test_vertex_get_rest(self, client: HiroClient):
        graph = client.rest.graph
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_vertex_get_data(self, client: HiroClient):
        graph = client.data.graph
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, dict)

    def test_vertex_get_model(self, client: HiroClient):
        graph = client.model.graph
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, Vertex)

    def test_vertex_update_rest(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.rest.graph
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v.id, {})
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_vertex_update_data(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.data.graph
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v.id, {})
        assert isinstance(res, dict)

    def test_vertex_update_model(self, client: HiroClient):
        graph = client.model.graph
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v, {})
        assert isinstance(res, Vertex)

    def test_vertex_delete_rest(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.rest.graph
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v.id)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_vertex_delete_data(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.data.graph
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v.id)
        assert isinstance(res, dict)

    def test_vertex_delete_model(self, client: HiroClient):
        graph = client.model.graph
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v)
        assert isinstance(res, Vertex)

    @pytest.mark.skip
    def test_vertex_history_rest(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.rest.graph
        pass

    @pytest.mark.skip
    def test_vertex_history_data(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.data.graph
        pass

    @pytest.mark.skip
    def test_vertex_history_model(self, client: HiroClient):
        graph = client.model.graph
        pass

    def test_edge_create_rest(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.rest.graph
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        req_data = {
            'out': str(vertex_a.id),
            'in': str(vertex_b.id),
        }
        edge_type = OgitVerb.OGIT_BELONGS.value.name.uri
        res = graph.edge.create(edge_type, req_data)
        res.raise_for_status()
        isinstance(res, Response)

    def test_edge_create_data(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.data.graph
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_type = OgitVerb.OGIT_BELONGS.value.name.uri
        res = graph.edge.create(vertex_a.id, edge_type, vertex_b.id)
        isinstance(res, dict)

    def test_edge_create_model(self, client: HiroClient):
        graph = client.model.graph
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_type = OgitVerb.OGIT_BELONGS
        res = graph.edge.create(vertex_a, edge_type, vertex_b)
        isinstance(res, Edge)

    def test_edge_delete_rest(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.rest.graph
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph_m.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c.id)
        res.raise_for_status()
        isinstance(res, Response)

    def test_edge_delete_data(self, client: HiroClient):
        graph_m = client.model.graph
        graph = client.data.graph
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph_m.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c.id)
        isinstance(res, dict)

    def test_edge_delete_model(self, client: HiroClient):
        graph = client.model.graph
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c)
        isinstance(res, Edge)


class TestClassFoo:
    @pytest.mark.skip
    def test_search_blob(self, client: HiroClient):
        search = client.model.search
        res = search.index(
            rf'+ogit\/_type:"{OgitEntity.OGIT_ATTACHMENT.id}"'
            r' -ogit\/_creator:"jharth@arago.co"'
            r' -ogit\/_creator:"mgrohrock@arago.co"'
            r' -ogit\/_creator:"cschulz@arago.co"'
        )
        import pprint
        for vertex in res:
            pprint.pprint(vertex.to_dict())

    @pytest.mark.skip
    def test_search_ts(self, client: HiroClient):
        search = client.model.search
        with search.index(
                rf'+ogit\/_type:"{OgitEntity.OGIT_TIME_SERIES.id}"'
                r' -\/DataName:"Time 99 percentile"'
        ) as res:
            yield from res


class TestClassSearch:
    def test_index_rest(self, client: HiroClient):
        search = client.rest.search
        res = search.index({'query': r'+ogit\/_id="ogit/Node"'})
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_index_data(self, client: HiroClient):
        search = client.data.search
        res = search.index(r'+ogit\/_id:"ogit/Node"')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)

    def test_index_model(self, client: HiroClient):
        search = client.model.search
        res = search.index(r'+ogit\/_id="ogit/Node"')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Vertex)

    def test_graph_rest(self, client: HiroClient):
        search = client.rest.search
        res = search.graph({'root': 'ogit/Node', 'query': 'out()'})
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_graph_data(self, client: HiroClient):
        search = client.data.search
        res = search.graph('ogit/Node', 'out()')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)

    def test_graph_model(self, client: HiroClient):
        search = client.model.search
        res = search.graph(VertexId('ogit/Node'), 'out()')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Vertex)

    def test_graph_model_2(self, client: HiroClient):
        search = client.model.search
        res = search.graph(VertexId('ogit/Node'), 'outE()', result_type=Edge)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Edge)


class TestClassStorage:
    @pytest.fixture
    def empty_blob_vertex(self, client: HiroClient) -> Generator[BlobVertex, None, None]:
        graph = client.model.graph
        vertex = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        yield vertex
        vertex.delete()

    @pytest.fixture
    def empty_ts_vertex(self, client: HiroClient) -> Generator[TimeSeriesVertex, None, None]:
        graph = client.model.graph
        vertex = graph.vertex.create(OgitEntity.OGIT_TIME_SERIES)
        yield vertex
        vertex.delete()

    @pytest.fixture
    def existing_ts_vertex(self, client: HiroClient) -> Generator[TimeSeriesVertex, None, None]:
        search = client.model.search
        res = search.index(
            rf'+ogit\/_type:"{OgitEntity.OGIT_TIME_SERIES.value.name.uri}"'
            r' -\/DataName:"Time 99 percentile"',
            limit=1
        )
        yield from res

    @pytest.fixture
    def isaac_asimov_birth_day(self) -> datetime:
        return datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc)

    def test_blob_set_rest(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.rest.storage
        res = storage.blob.set(empty_blob_vertex.id, png_img)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_blob_set_data(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.data.storage
        storage.blob.set(empty_blob_vertex.id, png_img)

    def test_blob_set_model(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.model.storage
        storage.blob.set(empty_blob_vertex, png_img)

    def test_blob_get_rest(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.rest.storage
        storage.blob.set(empty_blob_vertex.id, png_img)
        res = storage.blob.get(empty_blob_vertex.id)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_blob_get_data(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.data.storage
        storage.blob.set(empty_blob_vertex.id, png_img)
        res = storage.blob.get(empty_blob_vertex.id)
        assert isinstance(res, ContextManager)
        with res as g:
            assert isinstance(g, Generator)
            i = next(g)
            assert isinstance(i, bytes)

    def test_blob_get_model(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        storage = client.model.storage
        storage.blob.set(empty_blob_vertex, png_img)
        res = storage.blob.get(empty_blob_vertex)
        assert isinstance(res, ContextManager)
        with res as g:
            assert isinstance(g, Generator)
            i = next(g)
        assert isinstance(i, bytes)

    @pytest.mark.skip
    def test_log_get_rest(self, client: HiroClient):
        storage = client.rest.storage
        res = storage.log.get()
        res.raise_for_status()
        assert isinstance(res, Response)

    @pytest.mark.skip
    def test_log_get_data(self, client: HiroClient):
        storage = client.data.storage
        res = storage.log.get()
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)

    @pytest.mark.skip
    def test_log_get_model(self, client: HiroClient):
        storage = client.model.storage
        res = storage.log.get()
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Edge)

    def test_ts_get_rest(self, client: HiroClient, existing_ts_vertex: Vertex):
        storage = client.rest.storage
        res = storage.ts.get(existing_ts_vertex.id)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_ts_get_data(self, client: HiroClient, existing_ts_vertex: Vertex):
        storage = client.data.storage
        res = storage.ts.get(existing_ts_vertex.id)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)

    def test_ts_get_model(self, client: HiroClient, existing_ts_vertex: TimeSeriesVertex):
        storage = client.model.storage
        res = storage.ts.get(existing_ts_vertex)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, TimeSeriesValue)

    def test_ts_add_rest(self, client: HiroClient, empty_ts_vertex: Vertex):
        storage = client.rest.storage
        body = json.dumps({
            'timestamp': datetime_to_timestamp_ms(
                datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc)),
            'value': 'Isaac Asimov',
        })
        res = storage.ts.add(empty_ts_vertex.id, body)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_ts_add_data(self, client: HiroClient, empty_ts_vertex: Vertex):
        def g():
            yield {
                'timestamp': datetime_to_timestamp_ms(
                    datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc)),
                'value': 'Isaac Asimov',
            }

        storage = client.data.storage
        storage.ts.add(empty_ts_vertex.id, g())

    def test_ts_add_model(self, client: HiroClient, empty_ts_vertex: TimeSeriesVertex,
                          isaac_asimov_birth_day: datetime):
        def g():
            yield TimeSeriesValue(
                timestamp=datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc),
                value='Isaac Asimov',
            )

        storage = client.model.storage
        storage.ts.add(empty_ts_vertex, g())
        res = storage.ts.get(empty_ts_vertex,
                             start=datetime.combine(date.fromisoformat('1900-01-01'), time(), timezone.utc))
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, TimeSeriesValue)
