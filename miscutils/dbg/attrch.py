import re
from miscutils.func import permisive

def _get_meta(cls):
    if type(cls) is type:
        # cls does not have metaclass yet
        class Meta(type): pass
        class Medium(metaclass=Meta): pass
        meta_cls = Meta
        new_cls = type(cls.__qualname__, (cls, Medium), {})
    else:
        # cls has a metaclass already
        meta_cls = type(cls)
        new_cls = cls
    return new_cls, meta_cls

def _wrap_setattr(target, regex, macher, action):
    orig_setattr = getattr(target, '__setattr__', lambda name, value: setattr(target, name, value))
    def new_setattr(obj, name, value):
        orig_setattr(obj, name, value)
        if regex.match(name) and macher(value):
            action(name, value)
    target.__setattr__ = new_setattr

def attrch(name='.*', value=lambda val: True, action=lambda name, value: print(f'{name}={value}'), *, meta=False):
    """ Register an action to take on attribute change.

    def example1():

        # capture any attribute change
        @attrch()
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

    def example2():

        # capture any attribute change to 10
        # and changes of attributes of the name with two letters
        @attrch(value=10)
        @attrch('..')
        class Foo:
            pass

        foo = Foo()
        foo.x = 123
        foo.xy = 123
        foo.xyz = 10

    def example3():

        class M(type): pass

        @attrch('..', meta=True)
        class Foo(metaclass=M):
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123
        print(Foo)

    def example4():

        @attrch('..', meta=True)
        class Foo:
            pass

        Foo.x = 123
        Foo.xy = 123
        Foo.xyz = 123
        print(Foo)
    """
    regex = re.compile(name + '$')
    macher = value if callable(value) else lambda val: val == value

    def decorator(cls):
        if meta:
            return_cls, target_cls = _get_meta(cls)
        else:
            return_cls = target_cls = cls
        _wrap_setattr(target_cls, regex, macher, permisive(action))
        return return_cls

    return decorator

