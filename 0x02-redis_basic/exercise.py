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