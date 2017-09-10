import pytest
from functools import wraps
from miscutils.insp.experimental import arginfo

def test_features():

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        args = set(arginfo)
        assert args == {'p1', 'p2', 'p3', 'p4', 'p5', 'k1', 'k2', 'k3', 'k4', 'k5'}
        assert arginfo['p1'] == arginfo.p1
        assert 'p1' in arginfo
        assert arginfo['p3'].isset == arginfo.p3.isset
        assert arginfo['p3'].value == arginfo.p3.value
        assert arginfo['p3'].defval == arginfo.p3.defval
        assert str(arginfo['p3']) == 'Argument(defval=123, isset=True, value=33)'

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_in():

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        assert 'p1' in arginfo
        assert 'p2' in arginfo
        assert 'p3' in arginfo
        assert 'p4' in arginfo
        assert 'p5' in arginfo
        assert 'k1' in arginfo
        assert 'k2' in arginfo
        assert 'k3' in arginfo
        assert 'k4' in arginfo
        assert 'k5' in arginfo
        assert 'ar' not in arginfo
        assert 'kw' not in arginfo
        assert 'abc' not in arginfo
        assert '' not in arginfo
        assert None not in arginfo
        assert 123 not in arginfo

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)

def test_value():

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        assert arginfo.p1.value == 11
        assert arginfo.p2.value == 22
        assert arginfo.p3.value == 33
        assert arginfo.p4.value == 234
        assert arginfo.p5.value == 345
        assert arginfo.k1.value == 111
        assert arginfo.k2.value == 222
        assert arginfo.k3.value == 333
        assert arginfo.k4.value == 567
        assert arginfo.k5.value == 678

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_isset():

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        assert arginfo.p1.isset == True
        assert arginfo.p2.isset == True
        assert arginfo.p3.isset == True
        assert arginfo.p4.isset == True
        assert arginfo.p5.isset == False
        assert arginfo.k1.isset == True
        assert arginfo.k2.isset == True
        assert arginfo.k3.isset == True
        assert arginfo.k4.isset == True
        assert arginfo.k5.isset == False

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_defval():

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        assert hasattr(arginfo.p1, 'defval') == False
        assert hasattr(arginfo.p2, 'defval') == False
        assert arginfo.p3.defval == 123
        assert arginfo.p4.defval == 234
        assert arginfo.p5.defval == 345
        assert hasattr(arginfo.k1, 'defval') == False
        assert hasattr(arginfo.k2, 'defval') == False
        assert arginfo.k3.defval == 456
        assert arginfo.k4.defval == 567
        assert arginfo.k5.defval == 678

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_agent():

    def agent():
        assert arginfo.p3.isset == True
        assert arginfo.p3.value == 33
        assert arginfo.p3.defval == 123

    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        agent()

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_decorator():

    def deco(f):
        def wrpr(*a, **k):
            return f(*a, **k)
        return wrpr

    @deco
    @arginfo
    def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
        assert arginfo.p3.isset == True
        assert arginfo.p3.value == 33
        assert arginfo.p3.defval == 123

    foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_args_of_wrapper():

    def deco(f):
        def wrpr(p1, p2=321):
            return f(p1, p2)
        return wrpr

    @arginfo
    @deco
    def foo(p1, p2=123):
        assert arginfo.p2.defval == 321

    foo(0, 0)


def test_args_of_wrapper_wraps():

    def deco(f):
        @wraps(f)
        def wrpr(p1, p2=321):
            return f(p1, p2)
        return wrpr

    @arginfo
    @deco
    def foo(p1, p2=123):
        assert arginfo.p2.defval == 321

    foo(0, 0)


def test_regular_method():

    class C:
        @arginfo
        def foo(self, p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
            assert arginfo.p3.isset == True
            assert arginfo.p3.value == 33
            assert arginfo.p3.defval == 123

    c = C()
    c.foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_static_method():

    class C:
        @staticmethod
        @arginfo
        def foo(p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
            assert arginfo.p3.isset == True
            assert arginfo.p3.value == 33
            assert arginfo.p3.defval == 123

    c = C()
    c.foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)
    C.foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_class_method():

    class C:
        @classmethod
        @arginfo
        def foo(cls, p1, p2, p3=123, p4=234, p5=345, *ar, k1, k2, k3=456, k4=567, k5=678, **kw):
            assert arginfo.p3.isset == True
            assert arginfo.p3.value == 33
            assert arginfo.p3.defval == 123

    c = C()
    c.foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)
    C.foo(11, 22, 33, 234, k1=111, k2=222, k3=333, k4=567)


def test_recursive():

    entrance = 0

    @arginfo
    def foo(p1=123):
        nonlocal entrance
        entrance += 1

        if entrance == 1:
            assert arginfo.p1.isset == False
            assert arginfo.p1.value == 123
            assert arginfo.p1.defval == 123
            foo(100)
        elif entrance == 2:
            assert arginfo.p1.isset == True
            assert arginfo.p1.value == 100
            assert arginfo.p1.defval == 123
            foo(123)
        elif entrance == 3:
            assert arginfo.p1.isset == True
            assert arginfo.p1.value == 123
            assert arginfo.p1.defval == 123
        else:
            raise Exception("Too many calls")

    foo()


def test_multiple_func():

    @arginfo
    def bar(p1=321):
        assert arginfo.p1.defval == 321

    @arginfo
    def foo(p1=123):
        assert arginfo.p1.defval == 123
        bar()

    foo()


def test_deco_not_used():

    def foo(p1=123):
        arginfo.p1.value

    with pytest.raises(RuntimeError):
        foo()


def test_args_kwargs_simple():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        with pytest.raises(KeyError): arginfo.p
        with pytest.raises(KeyError): arginfo.k
        assert p == ()
        assert k == {}

    foo(0, k1=0)

def test_args_kwargs_kwarg_like_def_args():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.p.isset == True
        assert arginfo.p.value == ()
        with pytest.raises(KeyError): arginfo.k
        assert p == ()
        assert k == {'p': ()}

    foo(0, p=(), k1=0)

def test_args_kwargs_kwarg_like_tuple_args():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.p.isset == True
        assert arginfo.p.value == (123,)
        with pytest.raises(KeyError): arginfo.k
        assert p == ()
        assert k == {'p': (123,)}

    foo(0, p=(123,), k1=0)

def test_args_kwargs_kwarg_like_int_args():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.p.isset == True
        assert arginfo.p.value == 123
        with pytest.raises(KeyError): arginfo.k
        assert p == ()
        assert k == {'p': 123}

    foo(0, p=123, k1=0)

def test_args_kwargs_given_args():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        with pytest.raises(KeyError): arginfo.p
        with pytest.raises(KeyError): arginfo.k
        assert p == (123,)
        assert k == {}

    foo(0, 123, k1=0)

def test_args_kwargs_given_kwargs():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.kx.isset == True
        assert arginfo.kx.value == 123
        with pytest.raises(KeyError): arginfo.p
        with pytest.raises(KeyError): arginfo.k
        assert p == ()
        assert k == {'kx': 123}

    foo(0, k1=0, kx=123)

def test_args_kwargs_kwarg_like_def_kwargs():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.k.isset == True
        assert arginfo.k.value == {}
        with pytest.raises(KeyError): arginfo.p
        assert p == ()
        assert k == {'k': {}}

    foo(0, k1=0, k={})

def test_args_kwargs_kwarg_like_dict_kwargs():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.k.isset == True
        assert arginfo.k.value == {'kx': 123}
        with pytest.raises(KeyError): arginfo.p
        with pytest.raises(KeyError): arginfo.kw
        assert p == ()
        assert k == {'k': {'kx': 123}}

    foo(0, k1=0, k={'kx': 123})

def test_args_kwargs_kwarg_like_int_kwargs():
    @arginfo
    def foo(p1, *p, k1, **k):
        assert arginfo.p1.isset == True
        assert arginfo.k1.isset == True
        assert arginfo.k.isset == True
        assert arginfo.k.value == 123
        with pytest.raises(KeyError): arginfo.p
        assert p == ()
        assert k == {'k': 123}

    foo(0, k1=0, k=123)


#in operator

#def foo(p1, *, k1, **k):
    #pass

