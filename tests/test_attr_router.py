import pytest
from miscutils.attr_router import prompt

###################################################################################################################
# Proxy
###################################################################################################################

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

###################################################################################################################
# RouterLazy
###################################################################################################################

####################
# RouterLazy Reading
####################

def test_lazy_class_data_rd():

    class Foo:
        x = 123

    foo = Foo()
    rr = RouterLazy(foo)
    assert(rr.x == 123)

def test_lazy_object_data_rd():

    class Foo:
        pass

    foo = Foo()
    foo.x = 123
    rr = RouterLazy(foo)
    assert(rr.x == 123)

def test_lazy_class_data_object_data_rd():

    class Foo:
        x = 123

    foo = Foo()
    foo.x = 321
    rr = RouterLazy(foo)
    assert(rr.x == 321)

def test_lazy_object_prop_rd():

    class Foo:
        x = property(lambda obj: 123)

    foo = Foo()
    rr = RouterLazy(foo)
    assert(rr.x == 123)

def test_lazy_object_prop_object_data_rd():

    class Foo:
        pass

    foo = Foo()
    foo.x = 123
    Foo.x = property(lambda obj: 321)
    rr = RouterLazy(foo)
    assert(rr.x == 321)

####################
# RouterLazy Writing
####################

def test_lazy_data_wr():

    class Foo:
        pass

    foo = Foo()
    rr = RouterLazy(foo)
    rr.x = 123
    assert(foo.x == 123)

def test_lazy_prop_wr():

    class Foo:
        def set_x(self, val):
            self.x_val = val

        x = property(lambda obj: None, set_x)

    foo = Foo()
    rr = RouterLazy(foo)
    rr.x = 123
    assert(foo.x_val == 123)

####################
# RouterLazy Calling
####################

def test_lazy_class_meth_call():

    class Foo:
        def m(self):
            return 123

    foo = Foo()
    rr = RouterLazy(foo)
    assert(rr.m() == 123)

def test_lazy_object_meth_call():

    class Foo:
        pass

    foo = Foo()
    foo.m = lambda: 123
    rr = RouterLazy(foo)
    assert(rr.m() == 123)

######################
# RouterLazy Filtering
######################

def test_lazy_filter_regexp():

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterLazy(foo, '^x[0-1]$')
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_lazy_filter_bool():

    def qualifier(name):
        return name[-1] in '01'

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterLazyEx([ (foo, qualifier, lambda name: name) ])
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_lazy_filter_raise():

    def qualifier(name):
        assert(name[-1] in '01')
        return True

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterLazyEx([ (foo, qualifier, lambda name: name) ])
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_lazy_modif_regexp():
    class Foo:
        bar0 = 123
        bar1 = 321

    foo = Foo()
    rr = RouterLazy(foo, '^.*[a-zA-Z_]$', '^(.*)$', '\g<1>0')

    assert(rr.bar == 123)
    with pytest.raises(AttributeError):
        rr.bar0
    with pytest.raises(AttributeError):
        rr.bar1

def test_lazy_modif_custom():

    def modifier(name):
        return name.lower()

    class Foo:
        bar = 123

    foo = Foo()
    rr = RouterLazyEx([ (foo, lambda name: True, modifier) ])
    assert(rr.BAR == 123)
    assert(rr.Bar == 123)
    assert(rr.bar == 123)

######################
# RouterLazy Use Cases
######################

def test_lazy_uc_splitting():
    class Foo:
        bar0 = 123
        bar1 = 321

    foo = Foo()
    foo0 = RouterLazy(foo, '', '^(.*)$', '\g<1>0')
    foo1 = RouterLazy(foo, '', '^(.*)$', '\g<1>1')

    # test reads
    assert(foo0.bar == 123)
    assert(foo1.bar == 321)

    # test writes
    foo0.bar = 456
    foo1.bar = 567
    assert(foo.bar0 == 456)
    assert(foo.bar1 == 567)

def test_lazy_uc_combining():
    class Foo0:
        bar = 123

    class Foo1:
        bar = 321

    foo0 = Foo0()
    foo1 = Foo1()
    foo = RouterLazy(foo0, '^.*0$', '^(.*)0$', r'\1') + RouterLazy(foo1, '^.*1$', '^(.*)1$', r'\1')

    # test reads
    assert(foo.bar0 == 123)
    assert(foo.bar1 == 321)

    # test writes
    foo.bar0 = 345
    foo.bar1 = 456
    assert(foo0.bar == 345)
    assert(foo1.bar == 456)

def test_lazy_uc_nesting():
    class Foo0:
        bar0 = 123
        bar1 = 321

    class Foo1:
        bar0 = 456
        bar1 = 654

    foo0 = Foo0()
    foo1 = Foo1()

    hub = RouterLazy(foo0, '^foo0_.*$', '^foo0_(.*)$', r'\1') + RouterLazy(foo1, '^foo1_.*$', '^foo1_(.*)$', r'\1')
    bar0 = RouterLazy(hub, '^.*$', '^(.*)$', r'\1_bar0')
    bar1 = RouterLazy(hub, '^.*$', '^(.*)$', r'\1_bar1')

    # test reads
    assert(bar0.foo0 == 123)
    assert(bar0.foo1 == 456)
    assert(bar1.foo0 == 321)
    assert(bar1.foo1 == 654)

    # test writes
    bar0.foo0 = 1234
    bar0.foo1 = 4567
    bar1.foo0 = 3210
    bar1.foo1 = 6543
    assert(foo0.bar0 == 1234)
    assert(foo1.bar0 == 4567)
    assert(foo0.bar1 == 3210)
    assert(foo1.bar1 == 6543)

def test_lazy_add_eager():
    with pytest.raises(TypeError):
        RouterLazy(None) + RouterEager(None)

###################################################################################################################
# RouterEager
###################################################################################################################

#####################
# RouterEager Reading
#####################

def test_eager_class_data_rd():

    class Foo:
        x = 123

    foo = Foo()
    rr = RouterEager(foo)
    assert(rr.x == 123)

def test_eager_object_data_rd():

    class Foo:
        pass

    foo = Foo()
    foo.x = 123
    rr = RouterEager(foo)
    assert(rr.x == 123)

def test_eager_class_data_object_data_rd():

    class Foo:
        x = 123

    foo = Foo()
    foo.x = 321
    rr = RouterEager(foo)
    assert(rr.x == 321)

def test_eager_object_prop_rd():

    class Foo:
        x = property(lambda obj: 123)

    foo = Foo()
    rr = RouterEager(foo)
    assert(rr.x == 123)

def test_eager_object_prop_object_data_rd():

    class Foo:
        pass

    foo = Foo()
    foo.x = 123
    Foo.x = property(lambda obj: 321)
    rr = RouterEager(foo)
    assert(rr.x == 321)

#####################
# RouterEager Writing
#####################

def test_eager_data_wr():

    class Foo:
        x = 123

    foo = Foo()
    rr = RouterEager(foo)
    rr.x = 321
    assert(foo.x == 321)

def test_eager_prop_wr():

    class Foo:
        def set_x(self, val):
            self.x_val = val

        x = property(lambda obj: None, set_x)

    foo = Foo()
    rr = RouterEager(foo)
    rr.x = 123
    assert(foo.x_val == 123)

#####################
# RouterEager Calling
#####################

def test_eager_class_meth_call():

    class Foo:
        def m(self):
            return 123

    foo = Foo()
    rr = RouterEager(foo)
    assert(rr.m() == 123)

def test_eager_object_meth_call():

    class Foo:
        pass

    foo = Foo()
    foo.m = lambda: 123
    rr = RouterEager(foo)
    assert(rr.m() == 123)

def test_eager_dir_call():

    class Foo:
        x = 123
        y = property(lambda obj: None)
        def m(self): pass
        
    foo = Foo()
    foo.z = 123

    rr = RouterEager(foo)
    rr_dir = dir(rr)
    assert('x' in rr_dir)
    assert('y' in rr_dir)
    assert('z' in rr_dir)
    assert('m' in rr_dir)

#######################
# RouterEager Filtering
#######################

def test_eager_filter_regexp():

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterEager(foo, '^x[0-1]$')
    assert(set(dir(rr)) == {'x0', 'x1'})
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_eager_filter_bool():
    def qualifier(name):
        return name[-1] in '01'

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterEagerEx([ (foo, qualifier, lambda name: name) ])
    assert(set(dir(rr)) == {'x0', 'x1'})
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_eager_filter_raise():
    def qualifier(name):
        assert(name[-1] in '01')
        return True

    class Foo:
        x0 = 123
        x1 = 234
        x2 = 345
        x3 = 456

    foo = Foo()
    rr = RouterEagerEx([ (foo, qualifier, lambda name: name) ])
    assert(set(dir(rr)) == {'x0', 'x1'})
    assert(rr.x0 == 123)
    assert(rr.x1 == 234)
    with pytest.raises(AttributeError):
        rr.x2
    with pytest.raises(AttributeError):
        rr.x3

def test_eager_modif_regexp():
    class Foo:
        bar0 = 123
        bar1 = 321

    foo = Foo()
    rr = RouterEager(foo, '^[^_].*0$', '^(.*)[0-9]$', '\g<1>')

    assert(set(dir(rr)) == {'bar'})
    assert(rr.bar == 123)
    with pytest.raises(AttributeError):
        rr.bar0
    with pytest.raises(AttributeError):
        rr.bar1

def test_eager_modif_custom():
    def modifier(name):
        return name.upper()

    class Foo:
        bar = 123

    foo = Foo()
    rr = RouterEagerEx([ (foo, lambda name: True, modifier) ])
    assert(rr.BAR == 123)
    with pytest.raises(AttributeError):
        assert(rr.Bar)
    with pytest.raises(AttributeError):
        assert(rr.bar)

#######################
# RouterEager Use Cases
#######################

def test_eager_uc_splitting():

    class Foo:
        bar0 = 123
        bar1 = 321

    foo = Foo()
    foo0 = RouterEager(foo, '^.*0$', '^(.*)0$', '\g<1>')
    foo1 = RouterEager(foo, '^.*1$', '^(.*)1$', '\g<1>')

    # test dir()
    assert(dir(foo0) == ['bar'])
    assert(dir(foo1) == ['bar'])

    # test reads
    assert(foo0.bar == 123)
    assert(foo1.bar == 321)

    # test writes
    foo0.bar = 456
    foo1.bar = 567
    assert(foo.bar0 == 456)
    assert(foo.bar1 == 567)

def test_eager_uc_combining():

    class Foo0:
        bar = 123

    class Foo1:
        bar = 321

    foo0 = Foo0()
    foo1 = Foo1()
    foo = RouterEager(foo0, '^[^_].*$', '^(.*)$', r'\g<1>0') + RouterEager(foo1, '^[^_].*$', '^(.*)$', r'\g<1>1')

    # test dir()
    assert(set(dir(foo)) == {'bar0', 'bar1'})

    # test reads
    assert(foo.bar0 == 123)
    assert(foo.bar1 == 321)

    # test writes
    foo.bar0 = 345
    foo.bar1 = 456
    assert(foo0.bar == 345)
    assert(foo1.bar == 456)

def test_eager_uc_nesting():

    class Foo0:
        bar0 = 123
        bar1 = 321

    class Foo1:
        bar0 = 456
        bar1 = 654

    foo0 = Foo0()
    foo1 = Foo1()

    hub = RouterEager(foo0, '^[^_].*$', '^(.*)$', r'foo0_\1') + RouterEager(foo1, '^[^_].*$', '^(.*)$', r'foo1_\1')
    bar0 = RouterEager(hub, '^.*_bar0$', '^(.*)_bar0$', r'\1')
    bar1 = RouterEager(hub, '^.*_bar1$', '^(.*)_bar1$', r'\1')

    # test dir()
    assert(set(dir(bar0)) == {'foo0', 'foo1'})
    assert(set(dir(bar1)) == {'foo0', 'foo1'})

    # test reads
    assert(bar0.foo0 == 123)
    assert(bar0.foo1 == 456)
    assert(bar1.foo0 == 321)
    assert(bar1.foo1 == 654)

    # test writes
    bar0.foo0 = 1234
    bar0.foo1 = 4567
    bar1.foo0 = 3210
    bar1.foo1 = 6543
    assert(foo0.bar0 == 1234)
    assert(foo1.bar0 == 4567)
    assert(foo0.bar1 == 3210)
    assert(foo1.bar1 == 6543)

def test_eager_add_lazy():
    with pytest.raises(TypeError):
        RouterEager(None) + RouterLazy(None)



