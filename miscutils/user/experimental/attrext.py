
class AttrExt:
    """Enable child class to use attributes which are identified by non-string names. Also enable
       accessing attributes by indexing.

    Examples:

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

        >>> class Foo(AttrExt): pass
        >>> foo = Foo()
        >>> obj = object()
        >>> foo[123] = 'xyz'
        >>> foo[obj] = 'zyx'
        >>> foo[123]
        'xyz'
        >>> foo[obj]
        'zyx'

        >>> class Foo(AttrExt):
        ...     def bar(self):
        ...         print('Hello world!')
        >>> foo = Foo()
        >>> foo['bar']()
        Hello world!         
    """

    # stores attributes identified by non-string names
    _dictext = {}

    def __getitem__(self, name):
        if isinstance(name, str):
            return getattr(self, name)
        else:
            return self._dictext[name]

    def __setitem__(self, name, value):
        if isinstance(name, str):
            setattr(self, name, value)
        else:
            self._dictext[name] = value


