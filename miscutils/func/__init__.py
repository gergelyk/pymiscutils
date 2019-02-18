from time import sleep, time
from decorator import decorator
import inspect
import logging


log = logging.getLogger(__file__)
#logging.basicConfig(level=logging.DEBUG)


def catch(func):
    """Wrap the function to make sure that it doesn't raise any exception. Return wrapper function.
    Wrapper function accepts arguments and passes it to the wrapped function by calling it.
    If wrapped function raises an exception, exception will be returned by the wrapper.
    If wrapped function reuturns a value, wrapper will return an object of catch. ReturnValue
    type. Such object contains `value` member which provides value returned by the wrapped function.
    """
    class ReturnValue:
        def __init__(self, value):
            self.value = value
    catch.ReturnValue = ReturnValue

    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ReturnValue(ret)
        except Exception as ex:
            return ex
    return wrapper


def retry(max_attempts=5, interval=0.0, min_delay=0.0, deadline=None, exceptions=(Exception,)):
    """Decorator that retries calling unreliable functions
    max_attempts - maximum number of times that function can be called
    interval - intended interval between attempts (unless duration of the function call exceeds this interval)
    min_delay - minimum delay after one call is finished and before next call begins
    deadline - overal time allowed for making attempts (excluding duration of the last call)
    exceptions - exception type or tuple of types that specify on which exceptions re-try can be made
    """
    @decorator
    def retry_(func, *args, **kwargs):
        assert max_attempts >= 1
        assert interval >= 0
        assert min_delay >= 0
        func_name = func.__name__
        attempt = 0
        first_ts = time()
        current_ts = first_ts

        while True:
            last_ts = current_ts
            try:
                return func(*args, **kwargs)
            except exceptions as exc:

                log.debug(f"Exception occurred while calling {func_name!r}: {exc!r}")

                # check number of attempts
                attempt += 1
                if attempt >= max_attempts:
                    log.debug(f"Max number of {func_name!r} re-tries exceeded")
                    raise

                # check deadline
                current_ts = time()
                remaining_time = max(0, interval - (current_ts - last_ts))
                sleep_time = max(remaining_time, min_delay)
                if deadline is not None and current_ts + sleep_time - first_ts > deadline:
                    log.debug(f"Deadline for {func_name!r} exceeded")
                    raise

                # wait until interval remains
                sleep(sleep_time)
                log.debug(f"Retrying with {func_name!r}")

    return retry_

