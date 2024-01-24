#!/usr/bin/env python3
"""Redis Basic"""
import sys
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable
import redis
UnionOfTypes = Union[str, bytes, int, float]



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
