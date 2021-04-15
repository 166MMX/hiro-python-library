import io
from abc import ABC
from typing import Generator, Any, TypeVar, Iterable, Iterator, Optional

from ijson import items as ijson_items
from requests import Response


class AbcRest(ABC):
    __slots__ = ()


_T = TypeVar('_T')


def debug_iter(iterable: Iterable[_T], file_name: str) -> Generator[_T, None, None]:
    with open(file_name, 'wb') as f:
        for i in iterable:
            f.write(i)
            yield i


class AbcData(ABC):
    __slots__ = ()

    @staticmethod
    def items_generator(response: Response) -> Generator[Any, None, None]:
        with response:
            res_iter = response.iter_content(chunk_size=None)
            # res_iter = debug_iter(res_iter, 'http_response_bytes.json')
            readable = ReadableIterator(res_iter)
            item_iter = ijson_items(readable, prefix='items.item')
            yield from item_iter


class AbcModel(ABC):
    __slots__ = ()


class ReadableIterator(io.RawIOBase):
    # https://github.com/j-planet/Kaggle/blob/master/ValuedShoppers/IterStreamer.py
    def __init__(self, iterator: Iterator[bytes]) -> None:
        super().__init__()
        self.iterator = iterator
        self.partial_chunk = b''

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: bytearray) -> Optional[int]:
        buffer_size = len(buffer)
        chunk = bytearray(self.partial_chunk)

        while len(chunk) < buffer_size:
            try:
                b = next(self.iterator)
                chunk += b
            except StopIteration:
                stopped = True
                break
        else:
            stopped = False

        self.partial_chunk = chunk[buffer_size:]
        buffer[::] = chunk[:buffer_size]
        read = len(buffer)
        if read == 0 and stopped:
            self.close()
        return read
