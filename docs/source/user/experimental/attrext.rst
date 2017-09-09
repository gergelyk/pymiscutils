AttrExt
=======

**AttrExt** `()`

Enable child class to use attributes which are identified by non-string names. Also enable accessing attributes by indexing.

**Examples**

Attributes defined by string names.

>>> class Foo(AttrExt): pass
>>> foo = Foo()
>>> foo.abc = 123
>>> foo['bcd'] = 234
>>> setattr(foo, 'cde', 345)
>>> foo['abc']
123
>>> getattr(foo, 'bcd')
234
>>> foo.cde
345

Attributes defined by non-string names.

>>> class Foo(AttrExt): pass
>>> foo = Foo()
>>> obj = object()
>>> foo[123] = 'xyz'
>>> foo[obj] = 'zyx'
>>> foo[123]
'xyz'
>>> foo[obj]
'zyx'

Methods.

>>> class Foo(AttrExt):
...     def bar(self):
...         print('Hello world!')
>>> foo = Foo()
>>> foo['bar']()
Hello world!         


