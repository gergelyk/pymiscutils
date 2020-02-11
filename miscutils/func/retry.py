from time import sleep, time
from functools import wraps
import logging

log = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)

def retry(max_attempts=None, interval=0.0, min_delay=0.0, deadline=None, exceptions=(Exception,)):
    """Decorator that retries calling unreliable functions
    max_attempts - maximum number of times that function can be called, None means infinity
    interval - intended interval between attempts (unless duration of the function call exceeds this interval)
    min_delay - minimum delay after one call is finished and before next call begins
    deadline - overal time allowed for making attempts (excluding duration of the last call), None means infinity
    exceptions - exception type or tuple of types that specify on which exceptions re-try can be made
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert max_attempts is None or max_attempts >= 1
            assert interval >= 0
            assert min_delay >= 0
            try:
                func_name = func.__name__
            except AttributeError:
                func_name = repr(func)

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
                    if max_attempts is not None and attempt >= max_attempts:
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

        return wrapper
    return decorator

