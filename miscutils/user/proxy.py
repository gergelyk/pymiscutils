from types import new_class

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
