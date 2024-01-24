#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
from typing import Callable
from functools import wraps

redis_conn = redis.Redis()


def track_access_count(fn: Callable) -> Callable:
    """ Decorator to track the access count of a URL """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator """
        redis_conn.incr(f"count:{url}")
        return fn(url)

    return wrapper


def cache_page(fn: Callable) -> Callable:
    """
    Decorator to cache the result of func with a specified expiration time
    """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper for decorator """
        key = f"cached:{url}"

        # Check if the result is already in the cache
        cached_response = redis_conn.get(key)
        if cached_response:
            return cached_response.decode('utf-8')

        # If not in the cache, call the function and cache the result
        result = fn(url)
        redis_conn.setex(key, 10, result)
        return result

    return wrapper


@track_access_count
@cache_page
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL and returns it"""
    response = requests.get(url)
    return response.text


# Example usage:
url = "http://slowwly.robertomurray.co.uk"
html_content = get_page(url)
print(html_content)

# Check access count for the URL
access_count_key = f"count:{url}"
access_count = redis_conn.get(access_count_key)
print(f"{url} was accessed {access_count} times.")
