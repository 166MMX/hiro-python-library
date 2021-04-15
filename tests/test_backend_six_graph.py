from types import MappingProxyType
from typing import Generator, Optional, Type
from uuid import uuid4

import pytest

from arago.hiro.client.client import HiroClient
from arago.hiro.model.graph.attribute import FreeAttribute, SystemAttribute, FinalAttribute
from arago.hiro.model.graph.edge import Edge
from arago.hiro.model.graph.history import HistoryFormat, HistoryEntry, HistoryDiff
from arago.hiro.model.graph.vertex import VertexId, Vertex, ExternalVertexId, VERTEX_TYPE_T, VERTEX_T, VERTEX_T_co
# noinspection PyPackageRequirements
from arago.hiro.model.storage import TimeSeriesVertex, BlobVertex
from arago.ogit import OgitEntity, OgitVerb, OgitAttribute
from arago.ontology import Attribute


def uuid() -> str:
    return str(uuid4())


class TestClassGraphVertexCreate:
    @pytest.mark.parametrize('vertex_type', [
        OgitEntity.OGIT_COMMENT,
        OgitEntity.OGIT_COMMENT.value,
        OgitEntity.OGIT_COMMENT.value.name.uri
    ])
    def test_type_no_data(self, client: HiroClient, vertex_type: VERTEX_TYPE_T):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex = graph.vertex.create(vertex_type)
        assert isinstance(vertex, Vertex)
        vertex.delete()
        pass

    @pytest.mark.parametrize('vertex_type', [
        OgitEntity.OGIT_COMMENT,
        OgitEntity.OGIT_COMMENT.value,
        OgitEntity.OGIT_COMMENT.value.name.uri
    ])
    @pytest.mark.parametrize('vertex_data', [
        Vertex({OgitAttribute.OGIT_CONTENT: 'foo'}),
        BlobVertex({OgitAttribute.OGIT_CONTENT: 'foo'}),
        TimeSeriesVertex({OgitAttribute.OGIT_CONTENT: 'foo'}),
        {SystemAttribute.OGIT__XID: uuid()},
        {FinalAttribute.OGIT__XID: uuid()},
        {OgitAttribute.OGIT_CONTENT: 'foo'},
        {OgitAttribute.OGIT_CONTENT.value: 'foo'},
        {OgitAttribute.OGIT_CONTENT.value.name.uri: 'foo'},
        {FreeAttribute('/bar'): 'foo'},
    ])
    def test_type_data(self, client: HiroClient, vertex_type: VERTEX_TYPE_T, vertex_data: Optional[VERTEX_T]):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex = graph.vertex.create(vertex_type, vertex_data)
        assert isinstance(vertex, Vertex)
        vertex.delete()
        pass

    @pytest.mark.parametrize('vertex_data', [
        Vertex({
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            OgitAttribute.OGIT_CONTENT: 'foo'}),
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            SystemAttribute.OGIT__XID: uuid()},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            FinalAttribute.OGIT__XID: uuid()},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            OgitAttribute.OGIT_CONTENT: 'foo'},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            OgitAttribute.OGIT_CONTENT.value: 'foo'},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            OgitAttribute.OGIT_CONTENT.value.name.uri: 'foo'},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT,
            FreeAttribute('/bar'): 'foo'},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT.value,
            FreeAttribute('/bar'): 'foo'},
        {
            FinalAttribute.OGIT__TYPE: OgitEntity.OGIT_COMMENT.value.name.uri,
            FreeAttribute('/bar'): 'foo'},
    ])
    def test_data_no_type(self, client: HiroClient, vertex_data: Optional[VERTEX_T]):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex = graph.vertex.create(vertex_data)
        assert isinstance(vertex, Vertex)
        vertex.delete()
        pass

    @pytest.mark.parametrize('vertex_type,cls', [
        (OgitEntity.OGIT_TIME_SERIES, TimeSeriesVertex),
        (OgitEntity.OGIT_ATTACHMENT, BlobVertex),
    ])
    def test_upcast(self, client: HiroClient, vertex_type: VERTEX_TYPE_T, cls: Type[VERTEX_T_co]):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(vertex_type)
        assert isinstance(res, cls)
        res.delete()
        pass

    def test_ts(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(OgitEntity.OGIT_TIME_SERIES)
        assert isinstance(res, TimeSeriesVertex)
        res.delete()
        pass

    def test_blob_ogit(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        assert isinstance(res, BlobVertex)
        res.delete()
        pass

    def test_blob_ogit_map(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT, {
            OgitAttribute.OGIT_NAME: 'foo'
        })
        assert isinstance(res, BlobVertex)
        assert res[OgitAttribute.OGIT_NAME] == 'foo'
        res.delete()
        pass

    def test_blob_ogit_v(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT, Vertex({
            OgitAttribute.OGIT_NAME: 'foo'
        }))
        assert isinstance(res, BlobVertex)
        assert res[OgitAttribute.OGIT_NAME] == 'foo'
        res.delete()
        pass

    def test_blob_ontology(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        res = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT.value)
        assert isinstance(res, BlobVertex)
        res.delete()
        pass


class TestClassGraphVertexGet:
    def test_id(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_id = VertexId(OgitEntity.OGIT_COMMENT.value.name.uri)
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, Vertex)
        pass

    def test_str(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_id = OgitEntity.OGIT_COMMENT.value.name.uri
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, Vertex)
        pass

    def test_xid(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_id = ExternalVertexId('arago.co')
        res = graph.vertex.get(vertex_id)
        assert isinstance(res, Vertex)
        pass


class TestClassGraphVertexUpdate:
    def test_vertex_update_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.update(comment_v, {})
        assert isinstance(res, Vertex)
        pass


class TestClassGraphVertexDelete:
    def test_vertex_delete_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        comment_v = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.vertex.delete(comment_v)
        assert isinstance(res, Vertex)
        pass


class TestClassGraphVertexHistory:
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


class TestClassGraphEdgeCreate:
    def test_edge_create_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        res = graph.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        isinstance(res, Edge)
        pass


class TestClassGraphEdgeDelete:
    def test_edge_delete_model(self, client: HiroClient):
        from arago.hiro.backend.six.graph import Hiro6GraphModel
        graph = Hiro6GraphModel(client)
        vertex_a = graph.vertex.create(OgitEntity.OGIT_ATTACHMENT)
        vertex_b = graph.vertex.create(OgitEntity.OGIT_COMMENT)
        edge_c = graph.edge.create(vertex_a, OgitVerb.OGIT_BELONGS, vertex_b)
        res = graph.edge.delete(edge_c)
        isinstance(res, Edge)
        pass
