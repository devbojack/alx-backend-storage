#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests, redis
from functools import wraps

# Initialize Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def track_access_count(url):
    """
    Decorator to track the access count of a URL
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"count:{url}"
            redis_conn.incr(key)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def cache_page(expiration_time=10):
    """
    Decorator to cache the result of a function with a specified expiration time
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]
            key = f"cache:{url}"

            # Check if the result is already in the cache
            cached_result = redis_conn.get(key)
            if cached_result is not None:
                return cached_result

            # If not in the cache, call the function and cache the result
            result = func(*args, **kwargs)
            redis_conn.setex(key, expiration_time, result)
            return result
        return wrapper
    return decorator

@track_access_count("http://slowwly.robertomurray.co.uk")
@cache_page(expiration_time=10)
def get_page(url):
    """
    Retrieves the HTML content of a URL using the requests module
    """
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
