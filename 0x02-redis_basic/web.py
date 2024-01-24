#!/usr/bin/env python3
"""Expiring web cache module"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_conn = redis.Redis()


def track_access_count(fn: Callable) -> Callable:
    """Decorator to track the access count of a URL"""

    @wraps(fn)
    def wrapper(url):
        """Wrapper for decorator"""
        redis_conn.incr(f"count:{url}")
        return fn(url)

    return wrapper


def cache_page(expiration_time=10):
    """
    Decorator to cache the result of a function with
    a specified expiration time
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            key = f"cached:{url}"

            # Check if the result is already in the cache
            cached_response = redis_conn.get(key)
            if cached_response is not None:
                return cached_response.decode('utf-8')

            # If not in the cache, call the function and cache the result
            result = func(url)
            redis_conn.setex(key, expiration_time, result)
            return result
        return wrapper
    return decorator


@track_access_count
@cache_page(expiration_time=10)
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    response = requests.get(url)
    return response.text
