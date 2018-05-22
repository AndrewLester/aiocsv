import aiofiles
from collections import OrderedDict


def reader(aiofile, delimeter=',', quotechar='"'):
    return AioCSVReader(aiofile, delimeter, quotechar)


class AioCSVReader:
    def __init__(self, aiofile, delimeter, quotechar):
        self._aiofile = aiofile
        self._delimeter = delimeter
        self._quotechar = quotechar
        self.line_num = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        line = await self._aiofile.readline()
        if line:
            self.line_num += 1
            if not isinstance(line, str):
                raise TypeError('iterator should return strings, not bytes (did you open the file in text mode?)')
            return line.strip().replace(self._quotechar, '').split(self._delimeter)
        else:
            raise StopAsyncIteration

    next = __anext__


class AioDictReader(AioCSVReader):
    def __init__(self, aiofile, delimeter=',', quotechar='"'):
        super().__init__(aiofile, delimeter, quotechar)
        self.fieldnames = None

    async def __anext__(self):
        line = await super().__anext__()

        if self.fieldnames is None:
            self.fieldnames = line
            line_dict = await self.__anext__()
        else:
            line_dict = OrderedDict({k: v for (k, v) in zip(self.fieldnames, line)})

        return line_dict
