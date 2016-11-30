from miscutils.tree import tree
from textwrap import dedent

def test_simple():

    class C: pass
    c = C()
    setattr(c, 'foo.x', 123)
    setattr(c, 'foo.y', 234)
    setattr(c, 'bar.x', 345)
    setattr(c, 'bar.y', 456)
    s = tree(c)

    ref = """    
    bar
      x = 345
      y = 456
    foo
      x = 123
      y = 234
    """

    assert(dedent(ref).strip() == str(s))

def test_leaves_at_indices():

    class C: pass
    c = C()
    setattr(c, 'foo.x0', 123)
    setattr(c, 'foo.x1', 234)
    setattr(c, 'foo.x02', 345)
    s = tree(c)

    ref = """    
    foo
      x
        [0] = 123
        [1] = 234
        [2] = 345
    """
    
    assert(dedent(ref).strip() == str(s))

def test_branches_at_indices():

    class C: pass
    c = C()
    setattr(c, 'foo.x0.bar', 123)
    setattr(c, 'foo.x1.bar', 234)
    setattr(c, 'foo.x02.bar', 345)
    s = tree(c)

    ref = """    
    foo
      x
        [0]
          bar = 123
        [1]
          bar = 234
        [2]
          bar = 345
    """
    
    assert(dedent(ref).strip() == str(s))
    
def test_leaves_at_mixed():

    class C: pass
    c = C()
    setattr(c, 'foo.x0', 123)
    setattr(c, 'foo.x1', 234)
    setattr(c, 'foo.x02', 345)
    setattr(c, 'foo.x.bar', 456)
    s = tree(c)

    ref = """    
    foo
      x
        [0] = 123
        [1] = 234
        [2] = 345
        bar = 456
    """
    
    assert(dedent(ref).strip() == str(s))
    
def test_branches_at_mixed():

    class C: pass
    c = C()
    setattr(c, 'foo.x0.baz', 123)
    setattr(c, 'foo.x1.baz', 234)
    setattr(c, 'foo.x02.baz', 345)
    setattr(c, 'foo.x.bar.baz', 456)
    s = tree(c)

    ref = """    
    foo
      x
        [0]
          baz = 123
        [1]
          baz = 234
        [2]
          baz = 345
        bar
          baz = 456
    """
    
    assert(dedent(ref).strip() == str(s))
    
