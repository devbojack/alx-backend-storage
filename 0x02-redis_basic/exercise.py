#!/usr/bin/env python3
"""Redis Basic"""
import sys
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable
import redis
UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Counts how many times methods of the Cache class are called
    Takes a single method Callable argument
    Returns a Callable
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a particular function
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


def replay(cache, method: Callable) -> None:
    """Displays the history of calls for a particular function"""

    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    inputs = cache._redis.lrange(i, 0, -1)
    outputs = cache._redis.lrange(o, 0, -1)

    print(f"{key} was called {len(inputs)} times:")

    for input_str, output_str in zip(inputs, outputs):
        inputs_tuple = eval(input_str.decode("utf-8"))
        output = output_str.decode("utf-8")
        print(f"{key}(*{inputs_tuple}) -> {output}")


class Cache:
    """Cache class"""

    def __init__(self):
        """Cache class constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Takes a data argument
        Generate a random key
        Returns a string
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """Converts the data back to the desired format"""
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """Gets int"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Gets string"""
        return self.decode("utf-8")
