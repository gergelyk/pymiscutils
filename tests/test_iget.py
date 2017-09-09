import pytest
from miscutils.iter import iget

def test_genexp():
    g = range(10)
    assert iget(g, 5) == 5
    assert iget(g, 2) == 2

def test_genexp():
    def genfunc():
        while True:
            yield from range(10)

    g = genfunc()
    assert iget(g, 5) == 5
    assert iget(g, 2) == 8
    assert next(g) == 9

def test_genexp():
    g = range(10)
    with pytest.raises(IndexError):
        iget(g, 10)

