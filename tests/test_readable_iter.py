import io

import pytest
from arago.hiro.abc.common import ReadableIterator

from arago.hiro.client.client import HiroClient


@pytest.mark.skip
class TestClassReadableIterator:
    def test_io_base(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            with pytest.raises(io.UnsupportedOperation):
                readable.fileno()
            assert readable.closed is False
            readable.flush()
            assert readable.isatty() is False
            assert readable.readable() is True
            with pytest.raises(io.UnsupportedOperation):
                readable.seek(42)
            with pytest.raises(io.UnsupportedOperation):
                readable.tell()
            with pytest.raises(io.UnsupportedOperation):
                readable.truncate()
            assert readable.writable() is False
            with pytest.raises(NotImplementedError):
                # noinspection SpellCheckingInspection
                readable.writelines(b'c0ffebabe')
            res = readable.read(0)
            assert len(res) == 0
            assert readable.closed is False
            res = readable.read(1)
            assert len(res) == 1
            assert readable.closed is False
            res = readable.read(io.DEFAULT_BUFFER_SIZE - 42)
            assert len(res) == io.DEFAULT_BUFFER_SIZE - 42
            assert readable.closed is False

    def test_raw_io_base_write(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            with pytest.raises(NotImplementedError):
                readable.write(b'')

    def test_raw_io_base_read_default(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            res = readable.read()
            assert len(res) > io.DEFAULT_BUFFER_SIZE
            assert readable.closed is True

    def test_raw_io_base_readall(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            res = readable.readall()
            assert len(res) > 0
            assert readable.closed is True

    def test_io_base_readline(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            res = readable.readline()
            assert len(res) > 0
            assert readable.closed is True

    def test_io_base_readlines(self, client: HiroClient):
        with client.request(
                'POST', '/query/vertices',
                headers={'Accept': 'application/json'},
                json={'query': r'+ogit\/_id', 'limit': -1, 'offset': 0},
                stream=True
        ) as response:
            res_iter = response.iter_content(chunk_size=None)
            readable = ReadableIterator(res_iter)
            res = readable.readlines()
            assert len(res) == 1
            assert readable.closed is True
