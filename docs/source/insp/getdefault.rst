getdefault
==========
Get default value of the argument called ``argname`` from signature of the function ``func``.

For example:

>>> def foo(x, y, z=123):
...     pass
>>> getdefault(foo, 'z')
123
