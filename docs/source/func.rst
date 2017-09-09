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
