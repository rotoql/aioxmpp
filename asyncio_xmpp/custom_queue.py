import asyncio
import collections

class AsyncDeque:
    def __init__(self, initial_data=[], *, loop=None):
        super().__init__()
        self._data = collections.deque(initial_data)
        self._loop = loop
        self._non_empty = asyncio.Event()
        self._non_empty.clear()

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def put_nowait(self, value):
        self._data.append(value)
        if self._data:
            self._non_empty.set()

    def putleft_nowait(self, value):
        self._data.appendleft(value)
        if self._data:
            self._non_empty.set()

    def clear(self):
        self._data.clear()
        self._non_empty.clear()

    def extend(self, value):
        self._data.extend(value)
        if self._data:
            self._non_empty.set()

    def extendleft(self, value):
        self._data.extend(value)
        if self._data:
            self._non_empty.set()

    def empty(self):
        return bool(self._data)

    @asyncio.coroutine
    def getright(self):
        while not self._data:
            yield from self._non_empty.wait()
        result = self._data.pop()
        if not self._data:
            self._non_empty.clear()
        return result

    @asyncio.coroutine
    def get(self):
        while not self._data:
            yield from self._non_empty.wait()
        result = self._data.popleft()
        if not self._data:
            self._non_empty.clear()
        return result

    def get_nowait(self):
        try:
            return self._data.popleft()
        except IndexError:
            raise asyncio.QueueEmpty()

    def getright_nowait(self):
        try:
            return self._data.pop()
        except IndexError:
            raise asyncio.QueueEmpty()

    def remove(self, item):
        self._data.remove(item)
        if not self._data:
            self._non_empty.clear()
