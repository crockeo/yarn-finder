import functools
from typing import Callable, Coroutine
from typing import TypeVar


T = TypeVar("T")


def async_cache(
    callable: Callable[..., Coroutine[T]],
) -> Callable[..., Coroutine[T]]:
    """
    Provides a mechanism to cache the results of async functions.
    Currently caches the response globally, without considering arguments.
    """
    cached_result: T | None = None

    @functools.wraps(callable)
    async def _wrapper(*args, **kwargs) -> T:
        nonlocal cached_result
        if cached_result is None:
            cached_result = await callable(*args, **kwargs)
        return cached_result

    return _wrapper  # type: ignore
