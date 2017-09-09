from miscutils.user.experimental.attrext import AttrExt

def test_set_by_str_name():
    class Foo(AttrExt): pass
    foo = Foo()
    foo.abc = 123
    assert(foo.abc == 123)
    assert(foo['abc'] == 123)
    assert(getattr(foo, 'abc') == 123)

def test_set_by_str_index():
    class Foo(AttrExt): pass
    foo = Foo()
    foo['abc'] = 123
    assert(foo.abc == 123)
    assert(foo['abc'] == 123)
    assert(getattr(foo, 'abc') == 123)

def test_set_by_str_setattr():
    class Foo(AttrExt): pass
    foo = Foo()
    setattr(foo, 'abc', 123)
    assert(foo.abc == 123)
    assert(foo['abc'] == 123)
    assert(getattr(foo, 'abc') == 123)

def test_set_by_num_index():
    class Foo(AttrExt): pass
    foo = Foo()
    foo[999] = 123
    assert(foo[999] == 123)
    #assert(getattr(foo, 999) == 123)

# NOT ALLOWED
#def test_set_by_num_setattr():
#    class Foo(AttrExt): pass
#    foo = Foo()
#    setattr(foo, 999, 123)
#    assert(foo[999] == 123)
#    assert(getattr(foo, 999) == 123)

def test_set_by_obj_index():
    class Foo(AttrExt): pass
    foo = Foo()
    class Bar: pass
    bar = Bar()
    foo[bar] = 123
    assert(foo[bar] == 123)
    #assert(getattr(foo, 999) == 123)

# NOT ALLOWED
#def test_set_by_obj_setattr():
#    class Foo(AttrExt): pass
#    foo = Foo()
#    class Bar: pass
#    bar = Bar()
#    setattr(foo, bar, 123)
#    assert(foo[bar] == 123)
#    assert(getattr(foo, bar) == 123)

