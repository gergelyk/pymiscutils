insp
====

Utilities related to inspecting.

getdefault
----------
Get default value of the argument called ``argname`` from signature of the function ``func``.

For example:

>>> def foo(x, y, z=123):
...     pass
>>> getdefault(foo, 'z')
123

gloloc
------
Return dictionary which consists of items from globals() dict shadowed by items from locals() dict.

isaccess
------
Creates an object, attributes of which say if given name is specjal/private/protected/public according to Python convention.

For example:

>>> isaccess('_foo').protected
True
>>> isaccess('__bar__').public
False
>>> isaccess('baz').public
True
>>> str(isaccess('__qux__'))
'special'
