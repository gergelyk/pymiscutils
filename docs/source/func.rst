func
====

Utilities related to functions.

catch
-----
Wrap the function to make sure that it doesn't raise any exception. Return wrapper function.
Wrapper function accepts arguments and passes it to the wrapped function by calling it.
If wrapped function raises an exception, exception will be returned by the wrapper.
If wrapped function reuturns a value, wrapper will return an object of catch. ReturnValue
type. Such object contains ``value`` member which provides value returned by the wrapped function.

For example:

>>> from math import log10
>>> ret = catch(log10)(100)
>>> isinstance(ret, catch.ReturnValue)
True
>>> ret.value
2.0
>>> ret = catch(log10)(-100)
>>> isinstance(ret, catch.ReturnValue)
False
>>> ret
ValueError('math domain error')


retry
-----
Decorator that retries calling unreliable functions
max_attempts - maximum number of times that function can be called
interval - intended interval between attempts (unless duration of the function call exceeds this interval)
min_delay - minimum delay after one call is finished and before next call begins
deadline - overal time allowed for making attempts (excluding duration of the last call)
exceptions - exception type or tuple of types that specify on which exceptions re-try can be made

