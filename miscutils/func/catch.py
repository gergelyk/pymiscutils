from functools import wraps

def catch(func):
    """Wrap the function to make sure that it doesn't raise any exception. Return wrapper function.
    Wrapper function accepts arguments and passes it to the wrapped function by calling it.
    If wrapped function raises an exception, exception will be returned by the wrapper.
    If wrapped function reuturns a value, wrapper will return an object of catch. ReturnValue
    type. Such object contains `value` member which provides value returned by the wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            return ReturnValue(ret)
        except Exception as ex:
            return ex
    return wrapper

class ReturnValue:
    def __init__(self, value):
        self.value = value

catch.ReturnValue = ReturnValue
