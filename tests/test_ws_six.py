import pprint

from pytest import fixture

from arago.hiro.backend.six.graph_ws import HiroWebSocketClient


@fixture(scope='module')
def client():
    res = HiroWebSocketClient()
    res.connect(
        ''
        ''
        ''
        ''
    )
    return res


def test_get_vertex(client: HiroWebSocketClient):
    # noinspection SpellCheckingInspection
    vertex = client.get_vertex('ck8pwty3kks9pgx02ranrmdms')
    pprint.pprint(vertex)


def test_search_index(client: HiroWebSocketClient):
    vertices = client.search_index(r'_exists_:ogit\/_xid -ogit\/_creator:("jharth@arago.co" "cschulz@arago.co")')
    for vertex in vertices:
        pprint.pprint(vertex)
