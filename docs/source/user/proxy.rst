Proxy
=====

**Proxy** `(target, attr_names=None)`

Create dummy object which forwards attribute reads/writes to the target.

**Parameters**

    `target` - Any object.

    `attr_names` - Define list of available attributes. If ``None`` (default), then all the attributes of the target are accessible. Note that default list of available attributes is created when ``Proxy`` object is created.

**Returns**

    Proxy object.

**Examples**

>>> class Foo:
...     x = 123
>>> foo = Foo()
>>> foo.y = 321
>>> # create proxy object
>>> px = Proxy(foo)
>>> # read attributes
>>> px.x
123
>>> px.y
321
>>> # write attributes
>>> px.x = 999
>>> foo.x
999

