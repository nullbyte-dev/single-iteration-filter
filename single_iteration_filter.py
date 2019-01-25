""" Filter dataset partially in single iteration.
Dataset MUST be ordered before applying filtration.

>>> data = [
...     {'key': {0}},
...     {'key': {1}},
...     {'key': {1}},
...     {'key': {2}},
...     {'key': {3}},
...     {'key': {4}},
... ]
>>> keys = [(lambda x, y=y: x['key'] <= {y}) for y in range(6)]
>>> bounded = SingleIterationFilter(data)
>>> for i in bounded.apply(keys[0]):
...     print(i)
{'key': {0}}
>>> for i in bounded.apply(keys[1]):
...     print(i)
{'key': {1}}
{'key': {1}}
>>> for i in bounded.apply(keys[2]):
...     print(i)
{'key': {2}}
>>> for i in bounded.apply(keys[3]):
...     print(i)
{'key': {3}}
>>> for i in bounded.apply(keys[4]):
...     print(i)
{'key': {4}}
>>> for i in bounded.apply(keys[5]):
...     print(i)
"""
from typing import (
    Any,
    Iterator,
    Sequence,
    Callable,
)


class SingleIterationFilter:
    """ Encapsulate dataset & partially apply filtration """

    def __init__(self, data: Sequence) -> None:
        """ Make iterator over dataset & initialize values """
        self._data = iter(data)
        self._exit = False
        self._last = None

    def _next(self) -> Any:
        """ Just return next value from dataset """
        return next(self._data)

    def _filter(self, key: Callable) -> Iterator[Any]:
        """ Yields values from dataset if key(value) == True """
        try:
            item = self._last or self._next()
            while key(item):
                yield item
                item = self._next()
            self._last = item
        except StopIteration:
            self._last = None
            self._exit = True

    def apply(self, key: Callable) -> Iterator[Any]:
        """ Apply passed filter function to dataset """
        if self._exit:
            # do not fail on attempt applying filter
            # on exhausted dataset iterator
            return iter(())
        return self._filter(key)
