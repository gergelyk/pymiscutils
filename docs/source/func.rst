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

permisive
---------

Relax function signature

* Wrapped function behaves like all the ars were of `POSITIONAL_OR_KEYWORD` type, e.g.:

    .. code-block:: python

        func = lambda x, /, y, *, z: x * y + z
        5 == permisive(func)(1, 2, 3)
        5 == permisive(func)(z=3, y=1, x=2)
        7 == permisive(func)(3, 1, y=2)

* Arg of `VAR_POSITIONAL` type can be set using corresponding keyword, e.g.:

    .. code-block:: python

        func = lambda x, *ar: x * sum(ar)
        45 == permisive(func)(3, ar=(4, 5, 6))

* Arg of `VAR_KEYWORD` can be set using corresponding keyword, e.g.:

    .. code-block:: python

        func = lambda x, **kw: x * sum(kw.values())
        assert 45 == permisive(func)(3, kw=dict(a=4, b=5, c=6))

* Unnecessary args and kwargs are left unused, e.g.:

    .. code-block:: python

        func = lambda x, /, y, *, z: x * y + z
        assert 5 == permisive(func)(1, 2, 3, 4, 5) == 5
        assert 5 == permisive(func)(z=3, b=200, y=1, x=2, a=100) == 5

* This also plays well with default values, e.g.:

    .. code-block:: python

        func = lambda x=10, /, y=20, *, z=30: x * y + z
        assert  32 == permisive(func)(1, 2)
        assert  13 == permisive(func)(z=3, y=1)
        assert 230 == permisive(func)()

retry
-----
Decorator that retries calling unreliable functions
max_attempts - maximum number of times that function can be called
interval - intended interval between attempts (unless duration of the function call exceeds this interval)
min_delay - minimum delay after one call is finished and before next call begins
deadline - overal time allowed for making attempts (excluding duration of the last call)
exceptions - exception type or tuple of types that specify on which exceptions re-try can be made
