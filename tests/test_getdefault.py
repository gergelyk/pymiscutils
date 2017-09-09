import pytest
from miscutils.insp import getdefault

def uut(p1, p2=123, p3=Ellipsis, *a, k1, k2=456, **kw):
    pass

def test_p1():
    with pytest.raises(RuntimeError):
        getdefault(uut, 'p1')

def test_p2():
    assert getdefault(uut, 'p2') == 123

def test_p3():
    assert getdefault(uut, 'p3') == Ellipsis

def test_a():
    with pytest.raises(RuntimeError):
        getdefault(uut, 'a')

def test_k1():
    with pytest.raises(RuntimeError):
        getdefault(uut, 'k1')

def test_k2():
    assert getdefault(uut, 'k2') == 456

def test_kw():
    with pytest.raises(RuntimeError):
        getdefault(uut, 'kw')

def test_unknown():
    with pytest.raises(RuntimeError):
        getdefault(uut, 'unknown')

def test_not_argname():
    with pytest.raises(RuntimeError):
        getdefault(uut, 123)

def test_not_callable():
    with pytest.raises(TypeError):
        getdefault(123, 'unknown')
