from collections import UserDict

import pytest

from arago.hiro.model.graph.attribute import GraphType
from arago.hiro.model.graph.dict import GraphDict
from arago.hiro.model.storage import BlobId
from arago.ogit import OgitAttribute as OgitAttribute, OgitEntity, OgitVerb
from arago.ontology import OntologyEntity, OntologyVerb

OGIT__TYPE: OgitAttribute = OgitAttribute.OGIT__TYPE

OGIT__GRAPH_TYPE: OgitAttribute = OgitAttribute.OGIT__GRAPH_TYPE


def test_graph_dict_str():
    d = GraphDict({'ogit/_content': 'foobar'})
    assert isinstance(d, UserDict)
    assert isinstance(d, GraphDict)
    assert d['ogit/_content'] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT.value] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value.name.uri] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value] == 'foobar'


def test_graph_dict_ogit():
    d = GraphDict({OgitAttribute.OGIT__CONTENT: 'foobar'})
    assert isinstance(d, UserDict)
    assert isinstance(d, GraphDict)
    assert d['ogit/_content'] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT.value] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value.name.uri] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value] == 'foobar'


def test_graph_dict_onto():
    d = GraphDict({OgitAttribute.OGIT__CONTENT.value: 'foobar'})
    assert isinstance(d, UserDict)
    assert isinstance(d, GraphDict)
    assert d['ogit/_content'] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT] == 'foobar'
    assert d[OgitAttribute.OGIT__CONTENT.value] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value.name.uri] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE] == 'foobar'
    with pytest.raises(KeyError):
        assert d[OGIT__TYPE.value] == 'foobar'


@pytest.mark.skip
def test_graph_dict_get_id():
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX.value,
        OgitAttribute.OGIT__ID: 'foobar',
        OGIT__TYPE: OgitEntity.OGIT_ATTACHMENT,
    })
    vertex_id = d[OgitAttribute.OGIT__ID.value]
    assert vertex_id is not None
    print(type(vertex_id))
    assert isinstance(vertex_id, BlobId)


@pytest.mark.skip
def test_graph_dict_get_graph_type():
    d = GraphDict({OGIT__GRAPH_TYPE: 'vertex'})
    v = d[OGIT__GRAPH_TYPE]
    assert isinstance(v, GraphType)
    d = GraphDict({OGIT__GRAPH_TYPE: 'foo'})
    with pytest.raises(ValueError):
        v = d[OGIT__GRAPH_TYPE]
    d = GraphDict({OGIT__GRAPH_TYPE: GraphType.VERTEX})
    v = d[OGIT__GRAPH_TYPE]
    assert isinstance(v, GraphType)


@pytest.mark.skip
def test_graph_dict_get_type():
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX,
        OGIT__TYPE: 'ogit/Note'
    })
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyEntity)
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX,
        OGIT__TYPE: OgitEntity.OGIT_NOTE
    })
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyEntity)
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX,
        OGIT__TYPE: OgitEntity.OGIT_NOTE.value
    })
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyEntity)
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX,
        OGIT__TYPE: 123
    })
    with pytest.raises(TypeError):
        v = d[OGIT__TYPE]
    d = GraphDict({
        OGIT__GRAPH_TYPE: GraphType.VERTEX,
        OGIT__TYPE: 'foo'
    })
    with pytest.raises(ValueError):
        v = d[OGIT__TYPE]

    d = GraphDict({OGIT__TYPE: 'ogit/Note'})
    v = d[OGIT__TYPE]
    assert isinstance(v, str)
    assert v == 'ogit/Note'
    d = GraphDict({OGIT__TYPE: OgitEntity.OGIT_NOTE})
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyEntity)
    d = GraphDict({OGIT__TYPE: OgitEntity.OGIT_NOTE.value})
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyEntity)
    d = GraphDict({OGIT__TYPE: OgitVerb.OGIT_HAS})
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyVerb)
    d = GraphDict({OGIT__TYPE: OgitVerb.OGIT_HAS.value})
    v = d[OGIT__TYPE]
    assert isinstance(v, OntologyVerb)
    d = GraphDict({OGIT__TYPE: 123})
    v = d[OGIT__TYPE]
    assert isinstance(v, int)
    d = GraphDict({OGIT__TYPE: 'foo'})
    v = d[OGIT__TYPE]
    assert isinstance(v, str)
    d = GraphDict({OGIT__TYPE: GraphType.VERTEX})
    v = d[OGIT__TYPE]
    assert isinstance(v, GraphType)
