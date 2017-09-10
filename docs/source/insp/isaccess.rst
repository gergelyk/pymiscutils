isaccess
========
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
