import datetime
import time

import pytest

from arago.hiro.client.client import HiroClient


@pytest.mark.skip
class TestClassStreaming:
    # HTTPS_PROXY=127.0.0.1:8888
    def test_streaming_1(self, client: HiroClient):
        g = client.model.search.index(r'+ogit\/_id')  # contains _xid: None
        start = datetime.datetime.now()
        for v in g:
            t = datetime.datetime.now() - start
            print('%s: %s' % (t, v))

    def test_streaming_2(self, client: HiroClient):
        g = client.model.search.index(r'+ogit\/_id')  # contains _xid: None
        start = datetime.datetime.now()
        for v in g:
            t = datetime.datetime.now() - start
            print('%s: %s' % (t, v))

    def test_streaming_3(self, client: HiroClient):
        g = client.model.search.index(r'+ogit\/_id')  # contains _xid: None
        start = datetime.datetime.now()
        for v in g:
            t = datetime.datetime.now() - start
            print('%s: %s' % (t, v))

    def test_streaming_4(self, client: HiroClient):
        gen = client.model.search.index(r'+ogit\/_id')  # contains _xid: None
        start = time.time_ns()
        lst = list(gen)
        t = time.time_ns() - start
        print('%i: %s' % (t, len(lst)))
        start = time.time_ns()
        for v in lst:
            t = time.time_ns() - start
            print('%i: %s' % (t, v))
