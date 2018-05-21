import aiofiles
from collections import OrderedDict
import asyncio


def reader(aiofile, delimeter=',', quotechar='"', encoding='ascii'):
    return AioCSVReader(aiofile, delimeter, quotechar, encoding)


class AioCSVReader:
    def __init__(self, aiofile, delimeter, quotechar, encoding):
        self._aiofile = aiofile
        self._delimeter = delimeter
        self._quotechar = quotechar.encode(encoding)
        self._encoding = encoding
        self.line_num = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self._aiofile.readline()
        if line:
            self.line_num += 1
            return line.strip().replace(self._quotechar, b'').decode(self._encoding).split(self._delimeter)
        else:
            raise StopAsyncIteration

    next = __anext__


class AioDictReader(AioCSVReader):
    def __init__(self, aiofile, delimeter=',', quotechar='"', encoding='ascii'):
        super().__init__(aiofile, delimeter, quotechar, encoding)
        self.fieldnames = None

    async def __anext__(self):
        line = await super().__anext__()

        if self.fieldnames is None:
            self.fieldnames = line
            line_dict = await self.__anext__()
        else:
            line_dict = OrderedDict({k: v for (k, v) in zip(self.fieldnames, line)})

        return line_dict
