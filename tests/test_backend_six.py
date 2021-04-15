import json
from datetime import date, datetime, time, timezone
from types import MappingProxyType
from typing import Generator, ContextManager
from uuid import uuid4

# noinspection PyPackageRequirements
import pytest
from requests import Response

from arago.hiro.client.client import HiroClient
from arago.hiro.model.auth import SessionCredentials, AccessToken
from arago.hiro.model.graph.edge import Edge
from arago.hiro.model.graph.history import HistoryFormat, HistoryEntry, HistoryDiff
from arago.hiro.model.graph.vertex import VertexId, Vertex
from arago.hiro.model.storage import BlobVertex, TimeSeriesValue, TimeSeriesVertex
from arago.hiro.utils.datetime import datetime_to_timestamp_ms
from arago.ogit import OgitEntity, OgitVerb
from arago.ontology import Attribute


def uuid() -> str:
    return str(uuid4())


class TestClassMetaInfo:
    def test_info_rest(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaRest
        meta = Hiro6MetaRest(client)
        res = meta.info()
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_info_data(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaData
        meta = Hiro6MetaData(client)
        res = meta.info()
        assert isinstance(res, dict)
        pass

    def test_info_model(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaModel
        meta = Hiro6MetaModel(client)
        res = meta.info()
        assert isinstance(res, dict)
        pass

    def test_version_rest(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaRest
        meta = Hiro6MetaRest(client)
        with pytest.raises(NotImplementedError):
            res = meta.version()
            res.raise_for_status()
            assert isinstance(res, Response)
        pass

    def test_version_data(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaData
        meta = Hiro6MetaData(client)
        res = meta.version()
        assert isinstance(res, dict)
        pass

    def test_version_model(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaModel
        meta = Hiro6MetaModel(client)
        res = meta.version()
        assert isinstance(res, dict)
        pass

    def test_versions_rest(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaRest
        meta = Hiro6MetaRest(client)
        with pytest.raises(NotImplementedError):
            res = meta.versions()
            res.raise_for_status()
            assert isinstance(res, Response)
        pass

    def test_versions_data(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaData
        meta = Hiro6MetaData(client)
        res = meta.versions()
        assert isinstance(res, dict)
        pass

    def test_versions_model(self, client: HiroClient):
        from arago.hiro.backend.six.meta import Hiro6MetaModel
        meta = Hiro6MetaModel(client)
        res = meta.versions()
        assert isinstance(res, dict)
        pass


class TestClassHealth:
    def test_health_rest(self, client: HiroClient):
        from arago.hiro.backend.six.health import Hiro6HealthRest
        health = Hiro6HealthRest(client)
        res = health.check()
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_health_data(self, client: HiroClient):
        from arago.hiro.backend.six.health import Hiro6HealthData
        health = Hiro6HealthData(client)
        res = health.check()
        assert isinstance(res, dict)
        pass

    def test_health_model(self, client: HiroClient):
        from arago.hiro.backend.six.health import Hiro6HealthModel
        health = Hiro6HealthModel(client)
        res = health.check()
        assert isinstance(res, dict)
        pass


# noinspection PyUnusedLocal
class TestClassAuth:
    def test_token_get_rest(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthRest
        auth = Hiro6AuthRest(client)
        req_data = {
            'client_id': credentials.client.id,
            'client_secret': credentials.client.secret,
            'username': credentials.account.username,
            'password': credentials.account.password,
        }
        res = auth.password(req_data)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_token_get_data(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthData
        auth = Hiro6AuthData(client)
        res = auth.password(
            credentials.client.id,
            credentials.client.secret,
            credentials.account.username,
            credentials.account.password,
        )
        assert isinstance(res, dict)
        pass

    def test_token_get_model(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthModel
        auth = Hiro6AuthModel(client)
        res = auth.password(credentials)
        assert isinstance(res, AccessToken)
        pass

    @pytest.mark.skip
    def test_token_refresh_rest(self, client: HiroClient):
        from arago.hiro.backend.six.auth import Hiro6AuthRest
        auth = Hiro6AuthRest(client)
        pass

    @pytest.mark.skip
    def test_token_refresh_data(self, client: HiroClient):
        from arago.hiro.backend.six.auth import Hiro6AuthData
        auth = Hiro6AuthData(client)
        pass

    @pytest.mark.skip
    def test_token_refresh_model(self, client: HiroClient):
        from arago.hiro.backend.six.auth import Hiro6AuthModel
        auth = Hiro6AuthModel(client)
        pass

    def test_token_revoke_rest(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthRest
        auth = Hiro6AuthRest(client)
        req_data = {
            'client_id': credentials.client.id,
        }
        res = auth.revoke(req_data)
        res.raise_for_status()
        assert isinstance(res, Response)

    def test_token_revoke_data(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthData
        auth = Hiro6AuthData(client)
        auth.revoke(credentials.client.id)

    def test_token_revoke_model(self, client: HiroClient, credentials: SessionCredentials):
        from arago.hiro.backend.six.auth import Hiro6AuthModel
        auth = Hiro6AuthModel(client)
        auth.revoke(credentials.client)


class TestClassGraph:
    def test_vertex_create_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph = Hiro6GraphRest(client)
        vertex_type = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.create(vertex_type, {})
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_vertex_create_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph = Hiro6GraphData(client)
        vertex_type = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.create(vertex_type)
        assert isinstance(res, dict)
        pass

    def test_vertex_create_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_type = OgitEntity.OGIT_COMMENT
        res = graph.vertex.create(vertex_type)
        assert isinstance(res, Vertex)
        pass

    def test_vertex_get_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph = Hiro6GraphRest(client)
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_vertex_get_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph = Hiro6GraphData(client)
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, dict)
        pass

    def test_vertex_get_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_id = VertexId(OgitEntity.OGIT_COMMENT.value.name.uri)
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, Vertex)
        pass

    def test_vertex_update_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphRest(client)
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v.id, {})
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_vertex_update_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphData(client)
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v.id, {})
        assert isinstance(res, dict)
        pass

    def test_vertex_update_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v, {})
        assert isinstance(res, Vertex)
        pass

    def test_vertex_delete_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphRest(client)
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v.id)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_vertex_delete_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphData(client)
        comment_v = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v.id)
        assert isinstance(res, dict)
        pass

    def test_vertex_delete_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v)
        assert isinstance(res, Vertex)
        pass

    def test_vertex_history_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        res = client.root.model.search.index(rf'''ogit\/_type:"{OgitEntity.OGIT_LICENSE_REQUEST.value.name.uri!s}"''')
        vertex = next(res)
        graph = Hiro6GraphRest(client)
        v_res = graph.vertex.history(vertex.id)
        v_res.raise_for_status()
        assert isinstance(v_res, Response)
        pass

    def test_vertex_history_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphData
        res_1 = client.root.model.search.index(rf'''ogit\/_type:"{OgitEntity.OGIT_LICENSE_REQUEST.value.name.uri!s}"''')
        vertex = next(res_1)
        graph = Hiro6GraphData(client)
        res_2 = graph.vertex.history(vertex.id)
        assert isinstance(res_2, Generator)
        vertex = next(res_2)
        assert isinstance(vertex, dict)
        pass

    def test_vertex_history_model_element(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        res_1 = client.root.model.search.index(rf'''ogit\/_type:"{OgitEntity.OGIT_LICENSE_REQUEST.value.name.uri!s}"''')
        vertex = next(res_1)
        graph = Hiro6GraphModel(client)
        res_2 = graph.vertex.history(vertex, res_format=HistoryFormat.ELEMENT)
        assert isinstance(res_2, Generator)
        vertex = next(res_2)
        assert isinstance(vertex, Vertex)
        pass

    def test_vertex_history_model_full(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        res_1 = client.root.model.search.index(rf'''ogit\/_type:"{OgitEntity.OGIT_LICENSE_REQUEST.value.name.uri!s}"''')
        vertex = next(res_1)
        graph = Hiro6GraphModel(client)
        res_2 = graph.vertex.history(vertex, res_format=HistoryFormat.FULL)
        assert isinstance(res_2, Generator)
        entry = next(res_2)
        assert isinstance(entry, HistoryEntry)
        vertex = entry.data
        assert isinstance(vertex, Vertex)
        pass

    def test_vertex_history_model_diff(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        res_1 = client.root.model.search.index(rf'''ogit\/_type:"{OgitEntity.OGIT_LICENSE_REQUEST.value.name.uri!s}"''')
        vertex = next(res_1)
        graph = Hiro6GraphModel(client)
        res_2 = graph.vertex.history(vertex, res_format=HistoryFormat.DIFF)
        assert isinstance(res_2, Generator)
        diff = next(res_2)
        diff = next(res_2)
        assert isinstance(diff, HistoryDiff)
        replaced = diff.replaced
        assert isinstance(replaced, MappingProxyType)
        keys = iter(replaced)
        key = next(keys)
        assert isinstance(key, Attribute)
        pass

    def test_edge_create_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphRest(client)
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
        pass

    def test_edge_create_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphData(client)
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_type = OgitVerb.OGIT_BELONGS.value.name.uri
        res = graph.edge.create(vertex_a.id, edge_type, vertex_b.id)
        isinstance(res, dict)
        pass

    def test_edge_create_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_type = OgitVerb.OGIT_BELONGS
        res = graph.edge.create(vertex_a, edge_type, vertex_b)
        isinstance(res, Edge)
        pass

    def test_edge_delete_rest(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphRest
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphRest(client)
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph_m.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c.id)
        res.raise_for_status()
        isinstance(res, Response)
        pass

    def test_edge_delete_data(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        from arago.hiro.backend.six.graph import Hiro6GraphData
        graph_m = Hiro6GraphModel(client)
        graph = Hiro6GraphData(client)
        vertex_a = graph_m.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph_m.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph_m.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c.id)
        isinstance(res, dict)
        pass

    def test_edge_delete_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c)
        isinstance(res, Edge)
        pass


class TestClassFoo:
    @pytest.mark.skip
    def test_search_blob(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchModel
        search = Hiro6SearchModel(client)
        res = search.index(
            rf'+ogit\/_type:"{OgitEntity.OGIT_ATTACHMENT.id}"'
            r' -ogit\/_creator:"jharth@arago.co"'
            r' -ogit\/_creator:"mgrohrock@arago.co"'
            r' -ogit\/_creator:"cschulz@arago.co"'
        )
        import pprint
        for vertex in res:
            pprint.pprint(vertex.to_dict())
        pass

    @pytest.mark.skip
    def test_search_ts(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchModel
        search = Hiro6SearchModel(client)
        with search.index(
                rf'+ogit\/_type:"{OgitEntity.OGIT_TIME_SERIES.id}"'
                r' -\/DataName:"Time 99 percentile"'
        ) as res:
            yield from res
        pass


class TestClassSearch:
    def test_index_rest(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchRest
        search = Hiro6SearchRest(client)
        res = search.index({'query': r'+ogit\/_id="ogit/Node"'})
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_index_data(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchData
        search = Hiro6SearchData(client)
        res = search.index(r'+ogit\/_id:"ogit/Node"')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)
        pass

    def test_index_model(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchModel
        search = Hiro6SearchModel(client)
        res = search.index(r'+ogit\/_id="ogit/Node"')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Vertex)
        pass

    def test_graph_rest(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchRest
        search = Hiro6SearchRest(client)
        res = search.graph({'root': 'ogit/Node', 'query': 'out()'})
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_graph_data(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchData
        search = Hiro6SearchData(client)
        res = search.graph('ogit/Node', 'out()')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)
        pass

    def test_graph_model(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchModel
        search = Hiro6SearchModel(client)
        res = search.graph(VertexId('ogit/Node'), 'out()')
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Vertex)
        pass

    def test_graph_model_2(self, client: HiroClient):
        from arago.hiro.backend.six.search import Hiro6SearchModel
        search = Hiro6SearchModel(client)
        res = search.graph(VertexId('ogit/Node'), 'outE()', result_type=Edge)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Edge)
        pass


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
        from arago.hiro.backend.six.storage import Hiro6StorageRest
        storage = Hiro6StorageRest(client)
        res = storage.blob.set(empty_blob_vertex.id, png_img)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_blob_set_data(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        from arago.hiro.backend.six.storage import Hiro6StorageData
        storage = Hiro6StorageData(client)
        storage.blob.set(empty_blob_vertex.id, png_img)
        pass

    def test_blob_set_model(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        from arago.hiro.backend.six.storage import Hiro6StorageModel
        storage = Hiro6StorageModel(client)
        storage.blob.set(empty_blob_vertex, png_img)
        pass

    def test_blob_get_rest(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        from arago.hiro.backend.six.storage import Hiro6StorageRest
        storage = Hiro6StorageRest(client)
        storage.blob.set(empty_blob_vertex.id, png_img)
        res = storage.blob.get(empty_blob_vertex.id)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_blob_get_data(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        from arago.hiro.backend.six.storage import Hiro6StorageData
        storage = Hiro6StorageData(client)
        storage.blob.set(empty_blob_vertex.id, png_img)
        res = storage.blob.get(empty_blob_vertex.id)
        assert isinstance(res, ContextManager)
        with res as g:
            assert isinstance(g, Generator)
            i = next(g)
            assert isinstance(i, bytes)
            pass

    def test_blob_get_model(self, client: HiroClient, empty_blob_vertex: BlobVertex, png_img: bytes):
        from arago.hiro.backend.six.storage import Hiro6StorageModel
        storage = Hiro6StorageModel(client)
        storage.blob.set(empty_blob_vertex, png_img)
        res = storage.blob.get(empty_blob_vertex)
        assert isinstance(res, ContextManager)
        with res as g:
            assert isinstance(g, Generator)
            i = next(g)
        assert isinstance(i, bytes)
        pass

    @pytest.mark.skip
    def test_log_get_rest(self, client: HiroClient):
        from arago.hiro.backend.six.storage import Hiro6StorageRest
        storage = Hiro6StorageRest(client)
        res = storage.log.get()
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    @pytest.mark.skip
    def test_log_get_data(self, client: HiroClient):
        from arago.hiro.backend.six.storage import Hiro6StorageData
        storage = Hiro6StorageData(client)
        res = storage.log.get()
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)
        pass

    @pytest.mark.skip
    def test_log_get_model(self, client: HiroClient):
        from arago.hiro.backend.six.storage import Hiro6StorageModel
        storage = Hiro6StorageModel(client)
        res = storage.log.get()
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, Edge)
        pass

    def test_ts_get_rest(self, client: HiroClient, existing_ts_vertex: Vertex):
        from arago.hiro.backend.six.storage import Hiro6StorageRest
        storage = Hiro6StorageRest(client)
        res = storage.ts.get(existing_ts_vertex.id)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_ts_get_data(self, client: HiroClient, existing_ts_vertex: Vertex):
        from arago.hiro.backend.six.storage import Hiro6StorageData
        storage = Hiro6StorageData(client)
        res = storage.ts.get(existing_ts_vertex.id)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, dict)
        pass

    def test_ts_get_model(self, client: HiroClient, existing_ts_vertex: TimeSeriesVertex):
        from arago.hiro.backend.six.storage import Hiro6StorageModel
        storage = Hiro6StorageModel(client)
        res = storage.ts.get(existing_ts_vertex)
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, TimeSeriesValue)
        pass

    def test_ts_add_rest(self, client: HiroClient, empty_ts_vertex: Vertex):
        from arago.hiro.backend.six.storage import Hiro6StorageRest
        storage = Hiro6StorageRest(client)
        body = json.dumps({
            'timestamp': datetime_to_timestamp_ms(
                datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc)),
            'value': 'Isaac Asimov',
        })
        res = storage.ts.add(empty_ts_vertex.id, body)
        res.raise_for_status()
        assert isinstance(res, Response)
        pass

    def test_ts_add_data(self, client: HiroClient, empty_ts_vertex: Vertex):
        def g():
            yield {
                'timestamp': datetime_to_timestamp_ms(
                    datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc)),
                'value': 'Isaac Asimov',
            }

        from arago.hiro.backend.six.storage import Hiro6StorageData
        storage = Hiro6StorageData(client)
        storage.ts.add(empty_ts_vertex.id, g())
        pass

    def test_ts_add_model(self, client: HiroClient, empty_ts_vertex: TimeSeriesVertex,
                          isaac_asimov_birth_day: datetime):
        def g():
            yield TimeSeriesValue(
                timestamp=datetime.combine(date.fromisoformat('1920-01-02'), time(), timezone.utc),
                value='Isaac Asimov',
            )

        from arago.hiro.backend.six.storage import Hiro6StorageModel
        storage = Hiro6StorageModel(client)
        storage.ts.add(empty_ts_vertex, g())
        res = storage.ts.get(empty_ts_vertex,
                             start=datetime.combine(date.fromisoformat('1900-01-01'), time(), timezone.utc))
        assert isinstance(res, Generator)
        i = next(res)
        assert isinstance(i, TimeSeriesValue)
        pass
