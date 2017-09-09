iter
====

This module includes tools for acting with iterators and collections.

isfirst
-------

This class wrapps your iterator and turns it into another one, which iterates not only over the original data, but also over boolean flag which equals ``True`` for the first element and ``False`` for remaining elements.

For example:

>>> items = ['One', 'Two', 'Three']
>>> for item, first in isfirst(items):
...     if first:
...         print(item.upper())
...     else:
...         print(item)
ONE
Two
Three


islast
------

This class should be used by analogy to the one described in isfirst_. Please note that ``islast`` invokes ``len`` function on the original iterator, which means that the iterator must provide this functionality.

For example:

>>> items = ['One', 'Two', 'Three']
>>> for item, last in islast(items):
...     if last:
...         print(item.upper())
...     else:
...         print(item)
One
Two
THREE


isfirstlast
-----------

Wrappers ``isfirst`` and ``islast`` can be combined to provide cumulative functionality.

For example:

>>> items = ['One', 'Two', 'Three']
>>> for (item, first), last in islast(isfirst(items)):
...     if first:
...         print(item.upper())
...     elif last:
...         print(item.lower())
...     else:
...         print(item)
ONE
Two
three


Alternatively ``isfirstlast`` class can be used to get the same results and make syntax more readable.

For example:

>>> items = ['One', 'Two', 'Three']
>>> for item, first, last in isfirstlast(items):
...     if first:
...         print(item.upper())
...     elif last:
...         print(item.lower())
...     else:
...         print(item)
ONE
Two
three


iget
----

Get ``index``-nth element from iterable.

For example:

>>> g = range(10)
>>> iget(g, 5)
5

>>> def genfunc():
...     while True:
...         yield from 'abcd'
>>> g = genfunc()
>>> iget(g, 2)
'c'
