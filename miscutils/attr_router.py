import re
from types import new_class
from itertools import chain

class NoAttribute(AttributeError):
    """Object doesn't have attribute that is requested.
    """
    def __init__(self, obj, name):
        msg = "{} object has no attribute '{}'".format(type(obj).__name__, name)
        super().__init__(msg)

class CantAddObjects(TypeError):
    """Add operation is not available for given objects.
    """
    def __init__(self, obj, other):
        msg = "unsupported operand type(s) for +: '{}' and '{}'".format(type(obj).__name__, type(other).__name__)
        super().__init__(msg)

class Proxy:
    """Proxy(target, attr_names=None)

    Create dummy object which forwards attribute reads/writes to the target.

    Parameters
    ----------
    target : anything
        Any object.
    attr_names : list, optional
        Define list of available attributes. If None (default), then all the attributes of the
        target are accessible. Note that default list of available attributes is created when Proxy
        object is created.

    Returns
    -------
    out : Proxy
        Proxy object

    Examples:
    
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

    """
    def __new__(cls, target, attr_names=None):

        if attr_names == None:
            attr_names = dir(target)

        cls_dir = dir(cls)

        def __dir__(self):
            # Normally dir() would return only attributes of the Proxy object, but we want to
            # append also user-defined attributes
            full_dir = list(set(list(self.__dict__) + cls_dir + attr_names))
            return full_dir 

        def __getattr__(self, name):
            # If the name appears in dir(), it means that the attribute doesn't exist but we 
            # want to redirect the request to the target
            if name not in dir(self):
                msg = "'{}' object has no attribute '{}'".format(type(self).__name__, name)
                raise AttributeError(msg)
            return getattr(target, name)

        def __setattr__(self, name, value):
            # If existing attributes will be set on the target
            # Non-existing attribut will be created and set on the target
            return setattr(target, name, value)

        def body(ns):
            ns['__dir__'] = __dir__
            ns['__getattr__'] = __getattr__
            ns['__setattr__'] = __setattr__

        klass = new_class(cls.__name__, bases=(cls,), exec_body=body)
        obj = super().__new__(klass)
        return obj

class Router:
    """Parent class for the routers. Collects common pieces of code. Should not be instantiated.
    """
    def __getattr__(self, name):
        target, alias = self._convert_attr(name)
        return getattr(target, alias)

    def __setattr__(self, name, value):
        target, alias = self._convert_attr(name)
        setattr(target, alias, value)

    def __add__(self, other):
        # We support only adding two routers of the same kind

        bases = type(self).__bases__
        for base in bases:
            if not isinstance(other, base):
                raise CantAddObjects(self, other)

        klass = new_class(type(self).__name__, bases=bases )
        klass._rules = self._rules + other._rules
        obj = super().__new__(klass)
        return obj

def CreateNewRouter(cls, rules):
    """Creates dedicated Router class. Class like this has arbitrairly defined list of rules.
    """
    klass = new_class(cls.__name__, bases=(cls,) )
    klass._rules = rules
    obj = super(cls, cls).__new__(klass)
    return obj

def qualify(qualifier, name):
    """Runs function given as 'qualifier' with 'name' as argument. If exception occures, return
    False. Otherwise return whatever qualifier function returns.
    """
    try:
        return qualifier(name)
    except:
        return False

class RouterLazyEx(Router):
    """RouterLazyEx(rules)

    Router is an object, attributes of which are bound to the attributes of another (target) object.
    Router is responsible for translating between own namespace and the namespace of the target.
    
    Parameters
    ----------
    rules : list
        List of tuples where each one consist of the following elements:
        target : object
            Any object, methods of which can be accessed by the router.
        qualifier : callable
            Callable of the following prototype: qualifier(name).
            Qualifier is called on the name of attribute referenced by the user. Qualifier returns
            anything that evaluates to True if attribute should be accepted by the router.
            Otherwise qualifier returns anything that evaluates to False. For example 0, None,
            empty list, empty dict, etc. Alternatively qualifier can raise any exception in order
            to reject user's request.
        modifier : callable
            Callable of the following prototype: modifier(name).
            Modifier is called on the name of attribute referenced by the user. It translates the
            name to the one which will be used to access the target.

    Returns
    -------
    out : RouterLazyEx
        RouterLazyEx object

    Examples
    --------

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

    """
    def __new__(cls, rules):
        return CreateNewRouter(cls, rules)

    def _convert_attr(self, name):
        for target, qualifier, modifier in self._rules:
            if qualify(qualifier, name):
                break
        else:
            raise NoAttribute(self, name)

        return target, modifier(name)

class RouterEagerEx(Router):
    """RouterEagerEx(rules)

    Router is an object, attributes of which are bound to the attributes of another (target) object.
    Router is responsible for translating between own namespace and the namespace of the target.
    
    Parameters
    ----------
    rules : list
        List of tuples where each one consist of the following elements:
        target : object
            Any object, methods of which can be accessed by the router.
        qualifier : callable
            Callable of the following prototype: qualifier(name).
            Qualifier is called on the name of every attribute of the target. Qualifier returns
            anything that evaluates to True if attribute should be accepted by the router.
            Otherwise qualifier returns anything that evaluates to False. For example 0, None,
            empty list, empty dict, etc. Alternatively qualifier can raise any exception in order
            to discard the attribute.
        modifier : callable
            Callable of the following prototype: modifier(name).
            Modifier is called on the name of every qualified attribute. It translates the name
            of attribute of the target to the one which can be used by the user.

    Returns
    -------
    out : RouterEagerEx
        RouterEagerEx object

    Examples
    --------

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
    """
    def __new__(cls, rules):
        # For each rule do the following:
        # - qualify each attribute of the target against qualifier
        # - qualified attributes process uding modifier
        rules_processed = [(target, {modifier(name): name for name in dir(target) if qualify(qualifier, name)}) for target, qualifier, modifier in rules]
        
        # Results will be stores in _rules
        return CreateNewRouter(cls, rules_processed)

    def _convert_attr(self, name):
        for target, attr_names in self._rules:
            if name in attr_names:
                break
        else:
            raise NoAttribute(self, name)

        return target, attr_names[name]

    def __dir__(self):
        # extract attribute names from the rules
        all_names_2d = (attr_names for target, attr_names in self._rules)

        # combine them into one set
        all_names = {name for row in all_names_2d for name in row}

        # convert set into list and return
        return list(all_names)

def RouterLazy(target, selector='', pattern='', subst=''):
    """RouterLazy(target, selector='', pattern='', subst=''):

    Creates instance of RouterLazyEx with one rule which is build on regular expressions defined
    by selector, pattern and subst.
    
    Parameters
    ----------
    selector : string
        RegExp which defines which attributes refered by the user can be qualified.
    pattern : string
        RegExp which defines what in the name of the attribute is to be replaced before using it on the target.
    subst : string
        RegExp which defines how the name of the attribute is to be replaced before using it on the target.

    Returns
    -------
    out : RouterLazyEx
        RouterLazyEx object

    Examples
    --------

    Splitting object
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

    Combining objects
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

    Nested usage
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
    """
    return RouterLazyEx([ (target, lambda name: re.search(selector, name), lambda name: re.sub(pattern, subst, name)) ])

def RouterEager(target, selector='', pattern='', subst=''):
    """RouterEager(target, selector='', pattern='', subst=''):

    Creates instance of RouterEagerEx with one rule which is build on regular expressions defined
    by selector, pattern and subst.
    
    Parameters
    ----------
    selector : string
        RegExp which defines which attributes of the target can be qualified.
    pattern : string
        RegExp which defines what in the name of the attribute is to be replaced before making it available for the user.
    subst : string
        RegExp which defines how the name of the attribute is to be replaced before making it available for the user.

    Returns
    -------
    out : RouterEagerEx
        RouterEagerEx object

    Examples
    --------

    Splitting object
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

    Combining objects
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

    Nested usage
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

    """
    return RouterEagerEx([ (target, lambda name: re.search(selector, name), lambda name: re.sub(pattern, subst, name)) ])

