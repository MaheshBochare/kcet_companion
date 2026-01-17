import hashlib
from django.core.cache import cache

import hashlib
from django.core.cache import cache


def make_cache_key(prefix: str, *parts) -> str:
    """
    Creates a stable, Redis-safe cache key.

    Example:
        make_cache_key("cutoff_list", "GM", 1)
        -> cutoff_list:9e1f9a1c8c0d...

    This avoids very long keys and special character issues.
    """
    raw_key = ":".join(str(p) for p in parts)
    hashed = hashlib.md5(raw_key.encode("utf-8")).hexdigest()
    return f"{prefix}:{hashed}"


def get_or_set_cache(key: str, ttl: int, compute_func):
    """
    Fetch data from cache if exists, otherwise compute and store it.
    """
    data = cache.get(key)
    if data is not None:
        return data

    data = compute_func()
    cache.set(key, data, ttl)
    return data


