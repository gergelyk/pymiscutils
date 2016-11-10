Attribute Routers
=================

Attribute router is a dummy object which provides attributes of another object (target) to the user. Names of the attributes can be changed on the fly according to the rules defined in the router. This allows for distributing attributes of the target under different names across multiple objects. This will be referenced further as "splitting object".

Multiple routers of the same kind can be added, which results in a router containing superset of rules. This way it is possible to collect functionality provided by multiple objects. This will be referenced further as "combining objects".

There are two kinds of attribute routers:

**Lazy** - This router waits for the user to access it's attributes. Then it verifies if given attribute can be accepted. If yes, it translate the name of the attribute to the one which is specific to the target. Finally it accesses the attribute of the target.

Lazy routers have following advantages over eager routers:

* They can bound to the attributes of the target, which are not visible through ``dir()`` function. They may be defined as properties of emulated by ``__getattr__``, and ``__setattr__`` methods.
* Each attribute of the target can occur under multiple aliases through the router.

**Eager** - This router goes through the attributes of the target in advance. It verifies which attributes can be reffered to by the user. It also determines names under which the user will see the attributes of the target. Once this process is complete, the router waits for the user to access the attributes.

Eager routers have following advantages over lazy routers:

* ``dir()`` method called on the router returns list of methods that include aliases for the attributes. This is especially useful when you use interactive environments like IPython.
* As the router resolves rules in advance, in long term it is less CPU hungry.

Once you get familiar with the classess and functions below, please scroll to `Final Considerations`_ chapter to learn more about lazy and eager routers.

Proxy
-----

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

RouterLazyEx
------------

**RouterLazyEx** `(rules)`

Router is an object, attributes of which are bound to the attributes of another (target) object. Router is responsible for translating between own namespace and the namespace of the target.
    
**Parameters**

    `rules` - List of tuples where each one consist of the following elements:
        * target - Any object, methods of which can be accessed by the router.
        * qualifier - Callable of the following prototype: ``qualifier(name)``. Qualifier is called on the name of attribute referenced by the user. Qualifier returns anything that evaluates to True if attribute should be accepted by the router. Otherwise qualifier returns anything that evaluates to False. For example 0, ``None``, empty list, empty dict, etc. Alternatively qualifier can raise any exception in order to reject user's request.
        * modifier - Callable of the following prototype: ``modifier(name)``. Modifier is called on the name of attribute referenced by the user. It translates the name to the one which will be used to access the target.

**Returns**

    RouterLazyEx object.

**Examples**

>>> class Foo:
...     x0 = 123
...     x1 = 234
...     x2 = 345
...     x3 = 456
>>> foo = Foo()
>>> rr = RouterLazyEx([ (foo, lambda name: name[-1] in '01', lambda name: name.lower()) ])
>>> rr.x0
123
>>> rr.x1
234
>>> rr.X1
234
>>> rr.x2
NoAttribute: RouterLazyEx object has no attribute 'x2'
>>> rr.x3
NoAttribute: RouterLazyEx object has no attribute 'x3'

RouterEagerEx
-------------

**RouterEagerEx** `(rules)`

Router is an object, attributes of which are bound to the attributes of another (target) object. Router is responsible for translating between own namespace and the namespace of the target.
    
**Parameters**

    `rules` - List of tuples where each one consist of the following elements:
        * target - Any object, methods of which can be accessed by the router.
        * qualifier - Callable of the following prototype: ``qualifier(name)``. Qualifier is called on the name of every attribute of the target. Qualifier returns anything that evaluates to True if attribute should be accepted by the router. Otherwise qualifier returns anything that evaluates to False. For example 0, ``None``, empty list, empty dict, etc. Alternatively qualifier can raise any exception in order to discard the attribute.
        * modifier - Callable of the following prototype: ``modifier(name)``. Modifier is called on the name of every qualified attribute. It translates the name of attribute of the target to the one which can be used by the user.

**Returns**

    RouterEagerEx

**Examples**

>>> class Foo:
...     x0 = 123
...     x1 = 234
...     x2 = 345
...     x3 = 456
>>> 
>>> foo = Foo()
>>> rr = RouterEagerEx([ (foo, lambda name: name[-1] in '01', lambda name: name.upper()) ])
>>> dir(rr)
['X0', 'X1']
>>> rr.x0
NoAttribute: RouterEagerEx object has no attribute 'x0'
>>> rr.X0
123
>>> rr.X1
234
>>> rr.X2
NoAttribute: RouterEagerEx object has no attribute 'X2'
>>> rr.X3
NoAttribute: RouterEagerEx object has no attribute 'X3'


RouterLazy
----------

**RouterLazy** `(target, selector='', pattern='', subst='')`

Creates instance of RouterLazyEx with one rule which is build on regular expressions defined by selector, pattern and subst.
    
**Parameters**

    `selector` - RegExp which defines which attributes refered by the user can be qualified.
    `pattern` - RegExp which defines what in the name of the attribute is to be replaced before using it on the target.
    `subst` - RegExp which defines how the name of the attribute is to be replaced before using it on the target.

**Returns**

    RouterLazyEx object

**Examples**


Splitting object:

>>> class Foo:
...     bar0 = 123
...     bar1 = 321
>>> foo = Foo()
>>> foo0 = RouterLazy(foo, '', '^(.*)$', '\g<1>0')
>>> foo1 = RouterLazy(foo, '', '^(.*)$', '\g<1>1')
>>> foo0.bar
123
>>> foo1.bar
321

Combining objects:

>>> class Foo0:
...     bar = 123
>>> class Foo1:
...     bar = 321
>>> foo0 = Foo0()
>>> foo1 = Foo1()
>>> foo = RouterLazy(foo0, '^.*0$', '^(.*)0$', r'\1') + RouterLazy(foo1, '^.*1$', '^(.*)1$', r'\1')
>>> foo.bar0
123
>>> foo.bar1
321

Nested usage:

>>> class Foo0:
...     bar0 = 123
...     bar1 = 321
>>> class Foo1:
...     bar0 = 456
...     bar1 = 654
>>> foo0 = Foo0()
>>> foo1 = Foo1()
>>> hub = RouterLazy(foo0, '^foo0_.*$', '^foo0_(.*)$', r'\1') + RouterLazy(foo1, '^foo1_.*$', '^foo1_(.*)$', r'\1')
>>> bar0 = RouterLazy(hub, '^.*$', '^(.*)$', r'\1_bar0')
>>> bar1 = RouterLazy(hub, '^.*$', '^(.*)$', r'\1_bar1')
>>> bar0.foo0
123
>>> bar0.foo1
456
>>> bar1.foo0
321
>>> bar1.foo1
654

RouterEager
-----------

**RouterEager** `(target, selector='', pattern='', subst='')`

Creates instance of RouterEagerEx with one rule which is build on regular expressions defined by selector, pattern and subst.
    
**Parameters**
    `selector` - RegExp which defines which attributes of the target can be qualified.
    `pattern` - RegExp which defines what in the name of the attribute is to be replaced before making it available for the user.
    `subst` - RegExp which defines how the name of the attribute is to be replaced before making it available for the user.

**Returns**
    RouterEagerEx


**Examples**

Splitting object:

>>> class Foo:
...     bar0 = 123
...     bar1 = 321
>>> foo = Foo()
>>> foo0 = RouterEager(foo, '^.*0$', '^(.*)0$', '\g<1>')
>>> foo1 = RouterEager(foo, '^.*1$', '^(.*)1$', '\g<1>')
>>> dir(foo0)
['bar']
>>> dir(foo1)
['bar']
>>> foo0.bar
123
>>> foo1.bar
321

Combining objects:

>>> class Foo0:
...     bar = 123
>>> class Foo1:
...     bar = 321
>>> foo0 = Foo0()
>>> foo1 = Foo1()
>>> foo = RouterEager(foo0, '^[^_].*$', '^(.*)$', r'\g<1>0') + RouterEager(foo1, '^[^_].*$', '^(.*)$', r'\g<1>1')
>>> dir(foo)
['bar0', 'bar1']
>>> foo.bar0
123
>>> foo.bar1
321

Nested usage:

>>> class Foo0:
...     bar0 = 123
...     bar1 = 321
>>> class Foo1:
...     bar0 = 456
...     bar1 = 654
>>> foo0 = Foo0()
>>> foo1 = Foo1()
>>> hub = RouterEager(foo0, '^[^_].*$', '^(.*)$', r'foo0_\1') + RouterEager(foo1, '^[^_].*$', '^(.*)$', r'foo1_\1')
>>> bar0 = RouterEager(hub, '^.*_bar0$', '^(.*)_bar0$', r'\1')
>>> bar1 = RouterEager(hub, '^.*_bar1$', '^(.*)_bar1$', r'\1')
>>> dir(bar0)
['foo0', 'foo1']
>>> dir(bar1)
['foo0', 'foo1']
>>> bar0.foo0
123
>>> bar0.foo1
456
>>> bar1.foo0
321
>>> bar1.foo1
654

Final Considerations
--------------------

Qualifiers & Modifiers
~~~~~~~~~~~~~~~~~~~~~~

It is important to note that ``qualifiers`` and ``modifiers`` operate on different attributes in case of lazy and eager routers. For the lazy router, they qualify and process attribute names used by the user, while in case of the eager router they qualify and process attribute names specific to the target.

Adding routers of different types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is not possible to add routers of different types directly, however there are two workarounds possible. Let's consider following example:

>>> class Foo:
...     x = 123
>>> foo = Foo()
>>> r0 = RouterLazy(foo, '^lazy_(.*)$', '^lazy_(.*)$', r'\1')
>>> r1 = RouterEager(foo, '^[^_].*$', '^(.*)$', r'eager_\1')

We would like to combine functionality of r0 and r1. We keep in mind that r0 doesn't provide attributes of interest by ``dir()``, while r1 does. Our first option is to wrap r1 into lazy router, so that none of them provides attributes in ``dir()``.

>>> lazy = r0 + RouterLazy(r1)
>>> 'lazy_x' in dir(lazy)
False
>>> 'eager_x' in dir(lazy)
False
>>> lazy.lazy_x
123
>>> lazy.eager_x
123

Second option is to wrap the lazy router into eager one. For that however, we need to first manually assign list of attributes which lazy router provides. Here is where `Proxy` comes into play.

>>> eager = r1 + RouterEager(Proxy(r0, ['lazy_x']))
>>> 'lazy_x' in dir(eager)
True
>>> 'eager_x' in dir(eager)
True
>>> eager.lazy_x
123
>>> eager.eager_x
123




