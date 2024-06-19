import functools
import inspect


def response_wrapper(func):
    """
    wrap resposne context in result key
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)
        return {"result": result}

    return wrapper
