import pytest
from miscutils.routers import Proxy, RouterLazy

def test_proxy_dir_default():

    class Foo:
        x = 123

    foo = Foo()
    px = Proxy(foo)
    
    assert('x' in dir(px))

def test_proxy_dir_user():

    class Foo:
        x = 123

    foo = Foo()
    px = Proxy(foo, ['y'])
    
    assert('x' not in dir(px))
    assert('y' in dir(px))

def test_proxy_rd():

    class Foo:
        x = 123

    foo = Foo()
    px = Proxy(foo)
    
    assert(px.x == 123)

def test_proxy_wr():

    class Foo:
        x = 123

    foo = Foo()
    px = Proxy(foo)

    px.x = 321
    assert(foo.x == 321)

def test_proxy_wr_add():

    class Foo:
        x = 123

    foo = Foo()
    px = Proxy(foo, ['y'])

    px.y = 321
    px.z = 432
    assert(foo.y == 321)
    assert(foo.z == 432)

def test_proxy_uc_with_lazy_router():

    class Foo:
        x = 123
        y = 321

    foo = Foo()
    rr = RouterLazy(foo)
    px = Proxy(rr, ['x'])

    assert('x' in dir(px))
    assert('y' not in dir(px))
    assert(px.x == 123)
    with pytest.raises(AttributeError):
        px.y


