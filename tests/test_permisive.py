import pytest
from miscutils.func import permisive

def test_by_posargs():

    @permisive
    def func(a, b, c=30):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(1)

    assert func(1, 2) == (1, 2, 30)
    assert func(1, 2, 3) == (1, 2, 3)
    assert func(1, 2, 3, 4) == (1, 2, 3)

def test_by_kwargs():

    @permisive
    def func(a, b, c=30):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(a=1)

    assert func(a=1, b=2) == (1, 2, 30)
    assert func(a=1, b=2, c=3) == (1, 2, 3)
    assert func(a=1, b=2, c=3, d=4) == (1, 2, 3)

def test_by_posargs_posonly():

    @permisive
    def func(a, b, c=30, /):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(1)

    assert func(1, 2) == (1, 2, 30)
    assert func(1, 2, 3) == (1, 2, 3)
    assert func(1, 2, 3, 4) == (1, 2, 3)

def test_by_kwargs_posonly():

    @permisive
    def func(a, b, c=30, /):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(a=1)

    assert func(a=1, b=2) == (1, 2, 30)
    assert func(a=1, b=2, c=3) == (1, 2, 3)
    assert func(a=1, b=2, c=3, d=4) == (1, 2, 3)

def test_by_posargs_kwargsonly():

    @permisive
    def func(*, a, b, c=30):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(1)

    assert func(1, 2) == (1, 2, 30)
    assert func(1, 2, 3) == (1, 2, 3)
    assert func(1, 2, 3, 4) == (1, 2, 3)

def test_by_kwargs_kwargsonly():

    @permisive
    def func(*, a, b, c=30):
        return a, b, c

    with pytest.raises(TypeError):
        assert func(a=1)

    assert func(a=1, b=2) == (1, 2, 30)
    assert func(a=1, b=2, c=3) == (1, 2, 3)
    assert func(a=1, b=2, c=3, d=4) == (1, 2, 3)

def test_varargs_form_kword():

    @permisive
    def func(a, b, c=30, *d):
        return a, b, c, d

    assert func(1, 2, d=(3, 4)) == (1, 2, 30, (3, 4))
    assert func(1, 2, 33, d=(3, 4)) == (1, 2, 33, (3, 4))
    assert func(1, 2, 33, 44, d=(3, 4)) == (1, 2, 33, (3, 4))

def test_varargs_form_kword_posonly():

    @permisive
    def func(a, b, c=30, /, *d):
        return a, b, c, d

    assert func(1, 2, d=(3, 4)) == (1, 2, 30, (3, 4))
    assert func(1, 2, 33, d=(3, 4)) == (1, 2, 33, (3, 4))
    assert func(1, 2, 33, 44, d=(3, 4)) == (1, 2, 33, (3, 4))

def test_varargs_form_kword_kwargsonly():

    @permisive
    def func(*d, a, b, c=30):
        return a, b, c, d

    assert func(1, 2, d=(3, 4)) == (1, 2, 30, (3, 4))
    assert func(1, 2, 33, d=(3, 4)) == (1, 2, 33, (3, 4))
    assert func(1, 2, 33, 44, d=(3, 4)) == (1, 2, 33, (3, 4))

def test_kwargs_form_kword():

    @permisive
    def func(a, b, c=30, **d):
        return a, b, c, d

    assert func(1, 2, d={'d1': 3, 'd2': 4}) == (1, 2, 30, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, 44, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})

def test_kwargs_form_kword_posonly():

    @permisive
    def func(a, b, c=30, /, **d):
        return a, b, c, d

    assert func(1, 2, d={'d1': 3, 'd2': 4}) == (1, 2, 30, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, 44, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})

def test_kwargs_form_kword_kwargsonly():

    @permisive
    def func(*, a, b, c=30, **d):
        return a, b, c, d

    assert func(1, 2, d={'d1': 3, 'd2': 4}) == (1, 2, 30, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})
    assert func(1, 2, 33, 44, d={'d1': 3, 'd2': 4}) == (1, 2, 33, {'d1': 3, 'd2': 4})

def test_varargs_from_args():

    @permisive
    def func(a, b, c=30, *d):
        return a, b, c, d

    assert func(1, 2) == (1, 2, 30, ())
    assert func(1, 2, 3) == (1, 2, 3, ())
    assert func(1, 2, 3, 4) == (1, 2, 3, (4,))

def test_varargs_from_args_posonly():

    @permisive
    def func(a, b, c=30, /, *d):
        return a, b, c, d

    assert func(1, 2) == (1, 2, 30, ())
    assert func(1, 2, 3) == (1, 2, 3, ())
    assert func(1, 2, 3, 4) == (1, 2, 3, (4,))

def test_varargs_from_args_kwargsonly():

    @permisive
    def func(*d, a, b, c=30, ):
        return a, b, c, d

    assert func(a=1, b=2) == (1, 2, 30, ())
    assert func(a=1, b=2, c=3) == (1, 2, 3, ())
    assert func(4, a=1, b=2, c=3) == (1, 2, 3, (4,))

def test_empty():

    @permisive
    def func():
        return 999

    assert func() == 999

def test_complex():

    @permisive
    def func(a=-1, b=-1, /, c=-1, d=-1, *e, f=-1, g=-1, **h):
        return a, b, c, d, e, f, g, h

    assert func(f=2, c=1) == (-1, -1, 1, -1, (), 2, -1, {})
    assert func(1, 2, 3, 4, f=5, g=6) == (1, 2, 3, 4, (), 5, 6, {})
    assert func(1, 2, c=3, d=4, f=5, g=6) == (1, 2, 3, 4, (), 5, 6, {})
    assert func(1, 2, 3, 4, 5, 6, 7) == (1, 2, 3, 4, (5, 6, 7), -1, -1, {})
    assert func(1, 2, 3, 4, 5, e=(6, 7)) == (1, 2, 3, 4, (6, 7), 5, -1, {})
    assert func(1, 2, 3, 4, e=(11, 22, 33), h={'xx': 44, 'yy': 55, 'zz': 66}, f=5, g=6) == (1, 2, 3, 4, (11, 22, 33), 5, 6, {'xx': 44, 'yy': 55, 'zz': 66})

def test_examples1():
    func = lambda x, /, y, *, z: x * y + z
    assert 5 == permisive(func)(1, 2, 3)
    assert 5 == permisive(func)(z=3, y=1, x=2)
    assert 7 == permisive(func)(3, 1, y=2)

def test_examples2():
    func = lambda x, *ar: x * sum(ar)
    assert 45 == permisive(func)(3, ar=(4, 5, 6))

def test_examples3():
    func = lambda x, **kw: x * sum(kw.values())
    assert 45 == permisive(func)(3, kw=dict(a=4, b=5, c=6))

def test_examples4():
    func = lambda x, /, y, *, z: x * y + z
    assert 5 == permisive(func)(1, 2, 3, 4, 5) == 5
    assert 5 == permisive(func)(z=3, b=200, y=1, x=2, a=100) == 5

def test_examples5():
    func = lambda x=10, /, y=20, *, z=30: x * y + z
    assert  32 == permisive(func)(1, 2)
    assert  13 == permisive(func)(z=3, y=1)
    assert 230 == permisive(func)()
