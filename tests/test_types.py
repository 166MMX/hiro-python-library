import itertools
import json

import pytest

from arago.hiro.model.graph.attribute import FreeAttribute, SystemAttribute, VirtualAttribute, VirtualSystemAttribute, \
    ReadOnlyAttribute, FinalAttribute, GraphType, to_attribute
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.graph.vertex import Vertex, resolve_vertex_id, VertexId
from arago.ogit import OgitAttribute
from arago.ontology import OntologyAttribute


class TestClassVertex:
    def test_dict_round_trip(self):
        # noinspection SpellCheckingInspection
        d_a = json.loads(r'''{
  "ogit\/_created-on": 1585068142772,
  "\/ProcessIssue": "process_me",
  "ogit\/status": "TERMINATED",
  "ogit\/_modified-on": 1585069015158,
  "ogit\/_graphtype": "vertex",
  "ogit\/_owner": "arago.co",
  "ogit\/_v": 8,
  "ogit\/Automation\/deployStatus": "initialized",
  "ogit\/_modified-by-app": "cjix82tev000ou473gko8jgey",
  "ogit\/_type": "ogit\/Automation\/AutomationIssue",
  "ogit\/Automation\/suspendUntil": "2020-03-25 09:22:23.213112Z",
  "\/Counter": "1",
  "ogit\/Automation\/originNode": "ck0r9ti7f079qtv02hc4qsf28",
  "ogit\/_id": "ck864nagkv8qfgx02r2ybfoob",
  "ogit\/_creator": "ffluegel@arago.co",
  "ogit\/_v-id": "1585069015158-fmpmKq",
  "ogit\/subject": "",
  "ogit\/_is-deleted": false,
  "ogit\/_creator-app": "cjix82rxi000gu473w5kvkpqv",
  "ogit\/_modified-by": "hiro_engine",
  "ogit\/Automation\/processingTimestamp": "1585068143245"
}''')
        v = Vertex(d_a, draft=False)
        d_b = v.to_dict()
        for k_a, v_a in d_a.items():
            assert k_a in d_b.keys()
            v_b = d_b[k_a]
            assert v_a == v_b

    def test_attr_cast_free(self):
        a_1 = FreeAttribute('/foo')
        assert isinstance(a_1, FreeAttribute)

        a_2 = to_attribute('/foo')
        assert id(a_1) == id(a_2)

        a_3 = to_attribute(a_1)
        assert id(a_1) == id(a_3)

    def test_attr_cast_ogit(self):
        enum_member: OgitAttribute = OgitAttribute.OGIT_NAME
        a_1 = enum_member.value
        assert isinstance(a_1, OntologyAttribute)

        a_2 = to_attribute('ogit/name')
        assert id(a_1) == id(a_2)

        a_3 = to_attribute(enum_member)
        assert id(a_1) == id(a_3)

        a_4 = to_attribute(a_1)
        assert id(a_1) == id(a_4)

        with pytest.raises(ValueError):
            to_attribute('ogit/1415620a-8b4f-4a70-b093-73de0ec88371')

    def test_attr_cast_system(self):
        enum_member: OgitAttribute = OgitAttribute.OGIT__ID
        a_1 = enum_member.value
        assert isinstance(a_1, OntologyAttribute)

        a_2 = to_attribute('ogit/_id')
        assert id(a_1) == id(a_2)

        a_3 = to_attribute(enum_member)
        assert id(a_1) == id(a_3)

        a_4 = to_attribute(a_1)
        assert id(a_1) == id(a_4)

        a_5 = to_attribute(SystemAttribute.OGIT__ID)
        assert id(a_1) == id(a_5)

        with pytest.raises(ValueError):
            to_attribute('ogit/_1415620a-8b4f-4a70-b093-73de0ec88371')

    def test_attr_cast_virtual(self):
        enum_member: VirtualAttribute = VirtualAttribute.OGIT__OUT_ID
        a_1 = enum_member.value
        assert isinstance(a_1, VirtualSystemAttribute)

        a_2 = to_attribute(enum_member)
        assert id(a_1) == id(a_2)

        a_3 = to_attribute(a_1)
        assert id(a_1) == id(a_3)

        a_4 = to_attribute('ogit/_out-id')
        assert id(a_1) == id(a_4)

    def test_attr_cast_invalid(self):
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            to_attribute(123)
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            to_attribute(GraphType.VERTEX)
        with pytest.raises(ValueError):
            to_attribute('1415620a-8b4f-4a70-b093-73de0ec88371')

    def test_resolve_vertex_id(self):
        # def resolve_vertex_id(
        #         vertex: Union[None, Vertex, Mapping[Union[OgitAttribute, Attribute, str], Any]],
        #         vertex_id: Union[None, str, VertexId]
        # ) -> Optional[VertexId]:

        assert None is resolve_vertex_id(None, None)
        id_1 = VertexId('None')
        assert isinstance(id_1, VertexId)
        id_2 = resolve_vertex_id(None, 'None')
        assert id(id_1) == id(id_2)
        id_3 = resolve_vertex_id(None, id_1)
        assert id(id_1) == id(id_3)
        id_4 = resolve_vertex_id({
            'ogit/_id': 'None'
        }, None)
        assert id(id_1) == id(id_4)
        id_5 = resolve_vertex_id({
            OgitAttribute.OGIT__ID: 'None'
        }, None)
        assert id(id_1) == id(id_5)
        id_6 = resolve_vertex_id({
            OgitAttribute.OGIT__ID.value: 'None'
        }, None)
        assert id(id_1) == id(id_6)
        id_7 = resolve_vertex_id({
            OgitAttribute.OGIT__ID.value: id_1
        }, None)
        assert id(id_1) == id(id_7)
        id_7 = resolve_vertex_id({
            OgitAttribute.OGIT__ID.value: id_1
        }, None)
        assert id(id_1) == id(id_7)

    def test_graph_dict(self):
        for a, b in itertools.permutations((
                FinalAttribute.OGIT__ID, FinalAttribute.OGIT__ID.value,
                ReadOnlyAttribute.OGIT__ID, ReadOnlyAttribute.OGIT__ID.value,
                SystemAttribute.OGIT__ID, SystemAttribute.OGIT__ID.value,
                OgitAttribute.OGIT__ID, OgitAttribute.OGIT__ID.value,
                'ogit/_id', 'ogit:_id',
        ), 2):
            d = GraphDict({a: 'foo'})
            assert b in d
            assert 'foo' == d[b]
