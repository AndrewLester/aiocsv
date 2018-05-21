import aiofiles
from collections import OrderedDict
import asyncio


def reader(aiofile, delimeter=',', quotechar='"'):
    return AioCSVReader(aiofile, delimeter, quotechar)


class AioCSVReader:
    def __init__(self, aiofile, delimeter, quotechar):
        self._aiofile = aiofile
        self._delimeter = delimeter
        self._quotechar = quotechar

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self._aiofile.readline()
        if line:
            return line.strip().replace(self._quotechar.encode('ascii'), b'').decode('ascii').split(self._delimeter)
        else:
            raise StopAsyncIteration


class AioDictReader(AioCSVReader):
    def __init__(self, aiofile, delimeter=',', quotechar='"'):
        super().__init__(aiofile, delimeter, quotechar)
        self._header = None

    async def __anext__(self):
        line = await super().__anext__()

        if self._header is None:
            self._header = line
            line_dict = await asyncio.ensure_future(self.__anext__())
        else:
            line_dict = OrderedDict({k: v for (k, v) in zip(self._header, line)})

        return line_dict
