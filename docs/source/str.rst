str
===

Utilities related to strings.

lsub
----
**lsub** `(string, old, new='')`

If ``string`` starts with ``old`` replace ``old`` with ``new``. Return result.

For example:

>>> lsub('abcd', 'ab')
'cd'
>>> lsub('abcd', 'xy')
'abcd'
>>> lsub('abcd', 'ab', 'XY')
'XYcd'

rsub
----
**rsub** `(string, old, new='')`

If ``string`` ends with ``old`` replace ``old`` with ``new``. Return result.

>>> rsub('abcd', 'cd')
'ab'
>>> rsub('abcd', 'xy')
'abcd'
>>> rsub('abcd', 'cd', 'XY')
'abXY'
